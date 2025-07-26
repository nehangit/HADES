from planner.hierarchical_planner import HierarchicalPlanner
from manager.team_manager import TeamManager
from agents.sqli_agent import SQLiExpertAgent
from agents.xss_agent import XSSExpertAgent
from agents.csrf_agent import CSRFExpertAgent
from agents.ssti_agent import SSTIExpertAgent
from agents.zap_agent import ZAPExpertAgent
from agents.generic_agent import GenericWebHackingAgent
from utils.html_simplifier import simplify_html

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage


def main():
    # Get the input from the user
    print("[HPTSA] Web Application Exploitation System")
    url = input("Enter the target URL (default: http://localhost): ").strip()
    if not url:
        url = "http://localhost"
    print(f"[HPTSA] Using target URL: {url}")

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

    class MessagesState(dict):
        pass

    # Define the workflow graph
    workflow = StateGraph(MessagesState)
    workflow.add_node("planner", planner.node)
    workflow.add_node("manager", manager.node)
    for name, agent in agents.items():
        workflow.add_node(name, agent.node)
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "manager")
    for name in agents:
        workflow.add_edge("manager", name)
        workflow.add_edge(name, "manager")
    workflow.add_edge("manager", END)
    graph = workflow.compile()

    initstate = MessagesState({
        "target_url": url,
        "messages": [HumanMessage(content="Starting HPTSA workflow.")],
    })

    final_state = graph.invoke(initstate)
    print(final_state["messages"])

if __name__ == "__main__":
    main() 