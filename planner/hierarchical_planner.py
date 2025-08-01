from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from agents.tools_registry import ALL_TOOLS
from langchain_core.messages import HumanMessage

class HierarchicalPlanner:
    def __init__(self, model="gpt-4.1-mini"):
        self.llm = ChatOpenAI(model=model)
        self.agent = initialize_agent(
            tools=ALL_TOOLS,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True  # Helps avoid crashing on malformed tool outputs
        )

    def plan(self, url, extra_info):
        prompt = (
            "You are a web reconnaissance planner. Your role is to explore the target web application and discover points that can be exploited.\n"
            "Given the target URL, use your tools to identify:\n"
            "- Interesting pages (e.g., login, signup, profile, admin, search)\n"
            "- Input points (forms, parameters, cookies)\n"
            "- Potential vulnerability types (based on content and structure)\n\n"
            "The vulnerability types you are interested in include: \n"
            "- SQL Injection (SQLi)\n"
            "- Cross-Site Scripting (XSS)\n"
            "- Server-Side Template Injection (SSTI)\n"
            "- Cross-Site Request Forgery (CSRF)\n"
            "- Generic web vulnerabilities\n"
            "- Places to use OWASP ZAP scanning\n\n"
            "Then generate a prioritized plan consisting of web pages of interest and the reason for your interest in them.\n"
            "Each entry in the prioritized plan should include:\n"
            "- The specific page or input to test\n"
            "- The reason why it should be looked into\n"
            "Be concise and structured. Output the plan in this format:\n"
            "1. Investigate [PAGE/URL] because [REASON]\n"
            "2. ...\n\n"
            f"Target URL: {url}\n"
            "You are also provided the following extra information to aid you: \n"
            f"Extra Vulnerability Information: {extra_info}"
        )

        return self.agent.invoke({"input": prompt, "chat_history": []})['output']
    
    def node(self, state):
        url = state["target_url"]
        extra_info = state["extra_info"]
        plan = self.plan(url, extra_info)
        return {**state, "plan": plan, "messages": state.get("messages", []) + [HumanMessage(content=f"Plan: {plan}")]}
