from langchain_fireworks import ChatFireworks
from langchain.agents import initialize_agent, AgentType
from agents.tools_registry import ALL_TOOLS
from langchain_core.messages import HumanMessage

class HierarchicalPlanner:
    def __init__(self, model="accounts/fireworks/models/llama-v3p3-70b-instruct"):
        self.llm = ChatFireworks(model=model)
        self.agent = initialize_agent(
            tools=ALL_TOOLS,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )

    def plan(self, url):
        prompt = (
            "You are a web reconnaissance planner. Your role is to explore the target web application and discover points that can be exploited.\n"
            "Given the target URL, identify:\n"
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
            f"Target URL: {url}"
        )

        return self.agent.run(prompt)
    def node(self, state):
        url = state["target_url"]
        plan = self.plan(url)
        return {**state, "plan": plan, "messages": state.get("messages", []) + [HumanMessage(content=f"Plan: {plan}")]}
