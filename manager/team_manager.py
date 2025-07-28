from langchain_fireworks import ChatFireworks
from langchain.agents import initialize_agent, AgentType
from agents.tools_registry import ALL_TOOLS
from langchain_core.messages import HumanMessage
import json

class TeamManager:
    def __init__(self, model="accounts/fireworks/models/llama-v3p3-70b-instruct"):
        self.llm = ChatFireworks(model=model)
        self.agent = initialize_agent(
            tools=ALL_TOOLS,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )

    def coordinate(self, plan, results, target_url):

        prompt = (
            "You are the Team Manager in a hierarchical web exploitation system.\n\n"
            "You receive inputs from:\n"
            "- The planning agent (which lists prioritized targets like pages or input fields)\n"
            "- The outputs of previously run expert agents (which describe attempted payloads, observed behavior, and findings)\n\n"
            "Your job is to decide what to do next:\n"
            "1. Review the original prioritized plan and the already seen expert agent outputs.\n"
            "2. Determine which SINGLE expert agent should be invoked next (SQLi, XSS, CSRF, SSTI, ZAP, or Generic).\n"
            "3. Prepare a detailed instruction for that agent that includes everything it needs:\n"
            "- The target page or input field\n"
            "- Any credentials (if required)\n"
            "- Relevant prior findings or context\n"
            "- Specific goals or payload guidance\n\n"
            "Your output must be a JSON object in the following format:\n\n"
            "{\n"
            '  "agent": "AGENT_NAME",              # One of: "SQLi", "XSS", "CSRF", "SSTI", "ZAP", "GENERIC"\n'
            '  "instruction": "A clear instruction string for the agent with URLs, context, and goals."\n'
            "}\n\n"
            "Example output:\n"
            '{\n'
            '  "agent": "SQLi",\n'
            '  "instruction": "Test the login form at https://example.com/login using SQL injection techniques. '
            'Use the username `admin@example.com` and any password. '
            'The previous XSS agent found JavaScript errors when submitting malformed input, suggesting dynamic queries."\n'
            "}\n\n"
            "Be strategic: reuse findings to guide deeper attacks or shift attention to untested areas. "
            "Only one agent should be selected to be run.\n"
            "If you see any exploit succeeded in the expert agent output history, simply return output 'SUCCESS' and nothing else.\n"
            "If you believe there are no further avenues for exploitation, simply return output 'FAIL' and nothing else.\n"
            "Inputs: \n"
            f"Plan: \n{plan}\n"
            f"Previous Results: {results}\n"
            f"Base URL: {target_url}"
        )

        return self.agent.run(prompt)

    def node(self, state):
        plan = state["plan"]
        url = state["target_url"]
        results = state.get("results", [])
        decision = self.coordinate(plan, results, url)
        if decision == "SUCCESS" or decision == "FAIL":
            print(decision)
            return state, "END"
        else:
            try:
                decision_dict = json.loads(decision)
            except Exception as e:
                raise ValueError(f"Failed to parse manager decision as JSON: {decision}\nError: {e}")
            decision = decision_dict
        try:
            nextagent = decision["agent"]
            instruction = decision["instruction"]
            assert nextagent in ["SQLi", "XSS", "CSRF", "SSTI", "ZAP", "GENERIC"], "Generated bad agent name"
            messages = state.get("messages", []) + [HumanMessage(content=f"Decision: {decision}")]
            return {**state, "instruction": instruction, "messages": messages}, nextagent
        except Exception as e:
            raise ValueError(f"Bad manager decision object: {decision}\nError: {e}")