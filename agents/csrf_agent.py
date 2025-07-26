from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from agents.tools_registry import ALL_TOOLS
from langchain_core.messages import HumanMessage
import os

class CSRFExpertAgent:
    def __init__(self, model="gpt-4o"):
        self.llm = ChatOpenAI(model=model)
        self.agent = initialize_agent(
            tools=ALL_TOOLS,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )

    def run(self, target, instruction):
        prompt = (
            "You are a web exploitation expert specializing in CSRF (Cross-Site Request Forgery).\n"
            "You have been tasked with exploiting a specific page or input based on the following instruction:\n\n"
            f"{instruction}\n\n"
            "You should:\n"
            "- Use your expert knowledge and available tools to test for CSRF vulnerabilities\n"
            "- Attempt to exploit the target if feasible\n"
            "- Use automation, payload libraries, scanners, or manual reasoning as needed\n"
            "After your attempt, output a structured summary of what happened, using this format:\n\n"
            "{\n"
            '  "status": "success" | "fail" | "inconclusive",\n'
            '  "summary": "Concise description of what was attempted and observed",\n'
            '  "evidence": "Proof such as payloads used, error messages, reflected values, or screenshots/log URLs",\n'
            '  "recommendation": "Optional: suggest next steps if needed (e.g., retry with modified input, escalate to another agent)"\n'
            "}\n\n"
            "Be clear, technical, and truthful in your assessment. Your output will guide the next steps in the attack plan.\n"
            "Do not perform actions outside the provided instruction. Stay focused on CSRF.\n\n"
            f"Target: {target}"
        )
        return self.agent.run(prompt)

    def node(self, state):
        target_url = state.get("target_url", "http://localhost")
        instruction = state.get("instruction", f"Test CSRF vulnerabilities on {target_url}")
        result = self.run(target_url, instruction)
        
        # Update results in state
        results = state.get("results", [])
        results.append({
            "agent": "CSRF",
            "result": result
        })
        
        # Update messages
        messages = state.get("messages", []) + [HumanMessage(content=f"CSRF result: {result}")]
        
        return {**state, "results": results, "messages": messages}, "manager" 