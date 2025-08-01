from planner.hierarchical_planner import HierarchicalPlanner
from manager.team_manager import TeamManager
from agents.sqli_agent import SQLiExpertAgent
from agents.xss_agent import XSSExpertAgent
from agents.csrf_agent import CSRFExpertAgent
from agents.ssti_agent import SSTIExpertAgent
from agents.zap_agent import ZAPExpertAgent
from agents.generic_agent import GenericWebHackingAgent
from agents.tools_registry import session

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

def main():
    # Get the input from the user
    load_dotenv()
    print("[HPTSA] Web Application Exploitation System")
    url = input("Enter the target URL (default: http://localhost): ").strip()
    if not url:
        url = "http://localhost"
    print(f"[HPTSA] Using target URL: {url}")

    extrainfo = input("Enter any extra info to provide to the agents: ").strip()
    # Initialize the agents
    planner = HierarchicalPlanner()
    manager = TeamManager()
    agents = {
        "SQLi": SQLiExpertAgent(),
        "XSS": XSSExpertAgent(),
        "CSRF": CSRFExpertAgent(),
        "SSTI": SSTIExpertAgent(),
        "ZAP": ZAPExpertAgent(),
        "GENERIC": GenericWebHackingAgent(),
    }
    
    # Define the workflow graph
    workflow = StateGraph(dict)
    workflow.add_node("planner", planner.node)
    workflow.add_node("manager", manager.node)
    for name, agent in agents.items():
        workflow.add_node(name, agent.node)

    # workflow.add_edge(START, "manager")
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "manager")
    
    workflow.add_conditional_edges(
        "manager",
        lambda state: state["next"],
        ["SQLi", "XSS", "CSRF", "SSTI", "ZAP", "GENERIC", END],
    )

    for name in agents:
        workflow.add_edge(name, "manager")

    graph = workflow.compile()

    initstate = {
        "target_url": url,
        "extra_info": extrainfo,
        "messages": [HumanMessage(content="Starting HPTSA workflow.")],
    }
    try:
        final_state = graph.invoke(initstate)
        print(final_state["messages"])
        print(final_state["final_res"])
    except Exception as e:
        print(e)
        session.close()


if __name__ == "__main__":
    main() 