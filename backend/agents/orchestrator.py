from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Look for a file in previous directory too
from model import get_model, invoke_model
import json

load_dotenv()

model = get_model()


def orchestrator_node(state):
    """
    Supervises the whole travel planning system.

    The LLM only decides whether the current agent should retry.
    The orchestrator itself decides which agent runs next.
    """

    print("Calling agent orchestrator")

    replan_needed = state.get('replan_needed', False)
    plan_complete = state.get('plan_complete', False)
    report_complete = state.get('report_complete', False)
    research_complete = state.get('research_complete', False)

    retry_counts = state.get('retry_counts', {})
    current_agent = state.get('next_agent', 'research')

    orchestrator_feedback = state.get('orchestrator_feedback', "")

    flights = state.get('flights', [])
    trains = state.get('trains', [])
    hotels = state.get('hotels', [])
    itinerary = state.get('itinerary', [])

    # AGENT SEQUENCE
    sequence = {
        "research": "planner",
        "planner": "writer",
        "writer": "END"
    }

    # retry_counts represents how many times the current agent
    # has already been executed.
    # If current agent has been executed more than 2 times,
    # do NOT ask the LLM. Move to the next agent.

    current_retry_count = retry_counts.get(current_agent, 0)

    if current_retry_count > 2:

        next_agent = sequence.get(current_agent, "END")

        print(
            f"RETRY LIMIT EXCEEDED → "
            f"{current_agent} → {next_agent}"
        )

        return {
            **state,
            "next_agent": next_agent,
            "orchestrator_feedback": (
                f"{current_agent} retry limit exceeded. "
                f"Moving to {next_agent}."
            )
        }

    # IF EVERYTHING IS COMPLETE → END

    if report_complete:

        print("REPORT COMPLETE → END")

        return {
            **state,
            "next_agent": "END",
            "orchestrator_feedback": ""
        }

    # DETERMINE WHETHER THERE IS ACTUALLY A CURRENT AGENT

    # If starting the workflow
    if not research_complete:
        current_agent = "research"

    elif not plan_complete:
        current_agent = "planner"

    elif not report_complete:
        current_agent = "writer"

    # LLM EVALUATION

    eval_prompt = f"""
You are an orchestrator evaluating the performance of the CURRENT agent
in a travel planning system.

You must NOT decide which agent runs next.

Your ONLY task is to decide whether the CURRENT agent should be retried.

CURRENT AGENT:
{current_agent}

CURRENT STATE:

Research complete: {research_complete}

Flights found: {len(flights)} options

Trains found: {len(trains)} options

Hotels found: {len(hotels)} options

Plan complete: {plan_complete}

Itinerary days: {len(itinerary)}

Report complete: {report_complete}

Replan needed: {replan_needed}

Replan reason:
{state.get('replan_reason', '')}

Evaluate whether the CURRENT agent successfully completed its responsibility.

Rules:

1. If research_complete is False, the research agent has not completed
   its task, so retry the current agent.

2. If research_complete is True and plan_complete is False, the planner
   has not successfully completed the plan, so retry the current agent.

3. If replan_needed is True, the current plan needs revision, so retry
   the current agent.

4. If plan_complete is True and report_complete is False, the planner
   has completed its task and the writer should eventually handle the
   report. Therefore, the current agent should not be retried if the
   current agent is planner.

5. If report_complete is True, the workflow is complete and the current
   agent should not be retried.

6. Do not consider retry counts. Retry limits are handled by the
   orchestrator outside the LLM.

7. Do not decide the next agent.

Return ONLY valid JSON in exactly this structure:

{{
    "retry": true,
    "reason": "Clear explanation of why the current agent should or should not be retried.",
    "feedback": "Specific instruction for the current agent if it should retry."
}}

The value of "retry" MUST be a boolean:
true or false.

Do not return any other fields.
Do not use markdown.
Do not wrap the JSON in ```json.
"""

    output = invoke_model(model, eval_prompt)

    # PARSE LLM RESPONSE

    try:
        output = output.strip()
        if output.startswith("```json"):
            output = output[len("```json"):].strip()

        if output.endswith("```"):
            output = output[:-3].strip()

        raw = json.loads(output)

        retry = raw["retry"]
        reason = raw.get("reason", "")
        feedback = raw.get("feedback", "")

        # Make sure retry is actually boolean
        if not isinstance(retry, bool):
            raise ValueError(
                "'retry' must be a boolean true or false"
            )

    except Exception as e:

        print("Orchestrator JSON error:", e)
        print("Raw output:", output)

        # Safe fallback: do not retry if the orchestrator
        # cannot understand the LLM response.
        retry = False
        reason = "Failed to parse orchestrator decision."
        feedback = ""

    # DETERMINE NEXT AGENT

    if retry:
        next_agent = current_agent

        print(
            f"LLM DECISION → RETRY {current_agent}"
        )

    else:

        next_agent = sequence.get(current_agent, "END")

        print(
            f"LLM DECISION → MOVE {current_agent} → {next_agent}"
        )

    # UPDATE RETRY COUNTS

    retry_counts_new = retry_counts.copy()

    if retry:
        retry_counts_new[current_agent] = (
            retry_counts_new.get(current_agent, 0) + 1
        )

    # LOG STATE
    print(
        f"STATE → research={research_complete}, "
        f"plan={plan_complete}, "
        f"report={report_complete}, "
        f"current_agent={current_agent}, "
        f"retry={retry}"
    )

    print(f"NEXT AGENT → {next_agent}")


    # RETURN UPDATED STATE
    return {
        **state,
        "next_agent": next_agent,
        "orchestrator_feedback": feedback,
        "retry_counts": retry_counts_new,
    }