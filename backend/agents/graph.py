from typing import TypedDict,List,Optional,Any
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langgraph.graph import StateGraph,END,START
from agents.research import research_node
from agents.planner import plan_node
from agents.writer import write_node
from agents.orchestrator import orchestrator_node

class TravelState(TypedDict):
    # User input
    destination: str
    from_city: str
    start_date: str
    end_date: str
    budget: int
    group_size: int
    travel_mode: str
    preferences: list
    phone_number: str
    user_id: str
    departure_time: str
    arrival_time: str
    transit_state: str
    
    # Research output
    weather_data: dict
    flights: list
    trains: list
    hotels: list
    attractions: dict
    travel_tips: list
    research_complete: bool
    
    # Planner output
    itinerary: list
    budget_breakdown: dict
    replan_needed: bool
    replan_reason: str
    plan_complete: bool
    recommended_hotel:str
    recommended_flight_or_train: str
    total_estimated_cost: int
    
    # Orchestrator control
    next_agent: str
    orchestrator_feedback: str
    retry_counts: dict
    
    # Writer output
    formatted_report: str
    whatsapp_message: str
    calendar_events: list
    booking_links: dict
    report_complete: bool
    
def route_to_agent(state):
    next_agent=state.get('next_agent','research')
    return next_agent

def build_graph():
    
    graph=StateGraph(TravelState)
    
    # Added all nodes
    graph.add_node("research",research_node)
    graph.add_node("planner",plan_node)
    graph.add_node("writer",write_node)
    graph.add_node("orchestrator",orchestrator_node)
    
    # Starts from orchestrator
    graph.add_edge(START,"orchestrator")
    
    # Addimg the conditional edge 
    
    graph.add_conditional_edges(
        "orchestrator",route_to_agent,
        {
            "research":"research",
            "planner":"planner",
            "writer":"writer",
            "END":END
        }
    )
    
    # Adding edge back to orchestrator
    
    graph.add_edge("research","orchestrator")
    graph.add_edge("planner","orchestrator")
    graph.add_edge("writer","orchestrator")
    
    return graph.compile()

# Compiling the graph
travel_mind_graph=build_graph()