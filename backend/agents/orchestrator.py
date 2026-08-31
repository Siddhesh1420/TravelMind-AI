from dotenv import load_dotenv
import os
from groq import Groq
import json

load_dotenv()

api=os.getenv('GROQ_API_KEY')
model=Groq(api_key=api)

def orchestrator_node(state):
    """
    Supervises the whole travel planning system
    """
    
    replan_needed=state.get('replan_needed',False)
    plan_complete=state.get('plan_complete',False)
    report_complete=state.get('report_complete',False)
    research_complete=state.get('research_complete',False)
    retry_counts=state.get('retry_counts',{})
    orchestrator_feedback=state.get('orchestrator_feedback',"")
    
    flights=state.get('flights',[])
    trains=state.get('trains',[])
    hotels=state.get('hotels',[])
    report=state.get('formatted_report',"")
    itinerary=state.get('itinerary',[])
    
    eval_prompt = f"""You are an orchestrator supervising a travel planning system.

    Current state:
    - Research complete: {research_complete}
    - Flights found: {len(flights)} options
    - Trains found: {len(trains)} options  
    - Hotels found: {len(hotels)} options
    - Plan complete: {plan_complete}
    - Itinerary days: {len(itinerary)}
    - Report complete: {report_complete}
    - Replan needed: {replan_needed}
    - Replan reason: {state.get('replan_reason', '')}
    - Retry counts: {retry_counts}

    Rules:
    1. If research_complete is False → next_agent = "research"
    2. If research_complete is True but plan_complete is False → next_agent = "planner"
    3. If replan_needed is True and retry count for planner < 2 → next_agent = "planner" with feedback
    4. If plan_complete is True but report_complete is False → next_agent = "writer"
    5. If report_complete is True → next_agent = "END"
    6. If any agent has been retried 2+ times → force move to next agent

    Return ONLY valid JSON:
    {{
        "next_agent": "research" or "planner" or "writer" or "END",
        "feedback": "specific instruction for the next agent if retrying",
        "reason": "why you made this decision"
    }}"""
    
    response=model.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": eval_prompt}],
        max_tokens=4000,
        temperature=0.1
    )
    
    output=response.choices[0].message.content
    
    try:
        raw=json.loads(output)
    
        next_agent=raw['next_agent']
        feedback=raw.get('feedback',"")
    
    except (json.JSONDecodeError, Exception) as e:
        # If orchestrator node fails to parse
        next_agent="research"
        feedback="Orchestrator node failed to parse"
        
    retry_counts_new=retry_counts.copy()
    if next_agent in ['planner',"writer","research"]:
        retry_counts_new[next_agent]=retry_counts_new.get(next_agent,0)+1
        
    return {
        **state,
        'next_agent':next_agent,
        'orchestrator_feedback': feedback,
        "retry_counts":retry_counts_new,
    }
    