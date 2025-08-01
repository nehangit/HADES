from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from langgraph.graph import END
from typing import Literal, Union

class AgentInstruction(BaseModel):
    agent: Literal["SQLi", "XSS", "CSRF", "SSTI", "ZAP", "GENERIC"]
    instruction: str

class ManagerResponse(BaseModel):
    response: Union[AgentInstruction, Literal["SUCCESS", "FAIL"]]

class TeamManager:
    def __init__(self, model="gpt-4.1-mini"):
        self.llm = ChatOpenAI(model=model).with_structured_output(ManagerResponse)

    def coordinate(self, plan, results, target_url, extra_info):

        prompt = (
            "You are the Team Manager in a hierarchical web exploitation system.\n\n"
            "You receive inputs from:\n"
            "- The planning agent (which lists prioritized targets such as pages or input fields)\n"
            "- Outputs from previously run expert agents (describing attempted payloads, observed behavior, and findings)\n\n"
            "Your task:\n"
            "1. If any expert agent output indicates a successful exploit, respond with exactly:\n"
            "   SUCCESS\n"
            "2. If there are no further exploitation avenues, respond with exactly:\n"
            "   FAIL\n"
            "3. Otherwise, choose exactly one expert agent to run next from:\n"
            "   SQLi, XSS, CSRF, SSTI, ZAP, GENERIC\n"
            "4. Prepare a JSON object with the following format ONLY (no extra text):\n\n"
            "{\n"
            '  "agent": "AGENT_NAME",\n'
            '  "instruction": "Detailed instruction for the chosen agent including target page/input, credentials if any, prior findings, and goals."\n'
            "}\n\n"
            "Example:\n"
            '{\n'
            '  "agent": "SQLi",\n'
            '  "instruction": "Test the login form at https://example.com/login using SQL injection. Use username `admin@example.com` with any password. '
            'Note previous XSS agent found JavaScript errors on malformed input, indicating dynamic queries."\n'
            "}\n\n"
            "Be strategic: leverage prior findings to guide the next steps, or shift focus to untested areas.\n"
            "Do not output anything else except the JSON object.\n\n"
            "Inputs:\n"
            f"Plan:\n{plan}\n\n"
            f"Previous Results:\n{results}\n\n"
            f"Base URL: {target_url}\n"
            "You are also provided the following extra information to aid you: \n"
            f"Extra Vulnerability Information: {extra_info}"
        )

        return self.llm.invoke(prompt)

    def node(self, state):
        plan = state["plan"]
        url = state["target_url"]
        extra_info = state["extra_info"]
        results = state.get("results", [])
        decision = self.coordinate(plan, results, url, extra_info).response
        if isinstance(decision, str):
            return {**state, "final_res": decision, "next": END}
        try:
            nextagent = decision.agent
            instruction = decision.instruction
            assert nextagent in ["SQLi", "XSS", "CSRF", "SSTI", "ZAP", "GENERIC"], "Generated bad agent name"
            messages = state.get("messages", []) + [HumanMessage(content=f"Decision: {decision}")]
            return {**state, "instruction": instruction, "messages": messages, "next": nextagent}
        except Exception as e:
            raise ValueError(f"Bad manager decision object: {decision}\nError: {e}")