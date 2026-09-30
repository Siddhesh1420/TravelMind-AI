from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Look for a file in previous directory too
from model import get_model, invoke_model
import json
from prompts.orchestrator_prompt import get_orchestrator_prompt

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

    elif not plan_complete and not report_complete:
        current_agent = "planner"

    elif not report_complete:
        current_agent = "writer"

    # LLM EVALUATION

    eval_prompt = get_orchestrator_prompt(
    current_agent=current_agent,
    research_complete=research_complete,
    plan_complete=plan_complete,
    report_complete=report_complete,
    replan_needed=replan_needed,
    replan_reason=state.get('replan_reason', ''),
    flights=flights,
    trains=trains,
    hotels=hotels,
    itinerary=itinerary
)

    output = invoke_model(model, eval_prompt)
    
    if not output or output.strip() == "":
        return {
        **state,
        "next_agent": sequence.get(current_agent, "END"),
        "orchestrator_feedback": "LLM empty response — moving forward",
    }

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