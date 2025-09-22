"""
Pydantic AI - Simple 3 Agent Cycle (A -> B -> C -> A)
"""

from pydantic_ai import Agent
from typing import Dict, Any
import asyncio
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Agent A - Data Collector
agent_a = Agent(
    'openai:gpt-4.1-mini',
    system_prompt=(
        "You are Agent A - Data Collector. Your job is to collect and prepare initial data. "
        "When you receive data from Agent C, analyze it and prepare new data to send to Agent B. "
        "Always include 'processed_by': 'Agent_A' in your response."
    )
)

# Agent B - Data Processor  
agent_b = Agent(
    'openai:gpt-4.1-mini',
    system_prompt=(
        "You are Agent B - Data Processor. Your job is to process data from Agent A. "
        "Transform and enhance the data, then prepare it for Agent C. "
        "Always include 'processed_by': 'Agent_B' in your response."
    )
)

# Agent C - Data Analyzer
agent_c = Agent(
    'openai:gpt-4.1-mini',
    system_prompt=(
        "You are Agent C - Data Analyzer. Your job is to analyze processed data from Agent B. "
        "Provide insights and send summary back to Agent A to continue the cycle. "
        "Always include 'processed_by': 'Agent_C' in your response."
    )
)

async def run_agent_cycle():
    """Run the 3-agent cycle using programmatic handoff pattern"""
    
    # Initial data
    current_data = {
        "task": "Process customer feedback data",
        "data": ["Great product!", "Needs improvement", "Love the features"],
    }
    
    for cycle in range(2):
        print(f"\n--- Cycle {cycle + 1} ---")
        
        # Agent A processes data
        print("Agent A processing...")
        prompt_a = f"Process this data and prepare it for Agent B: {current_data}"
        result_a = await agent_a.run(prompt_a)
        print(f"Agent A result: {result_a.output}")
        
        # Agent B processes Agent A's output
        print("\nAgent B processing...")
        prompt_b = f"Process this data from Agent A and prepare for Agent C: {result_a.output}"
        result_b = await agent_b.run(prompt_b)
        print(f"Agent B result: {result_b.output}")
        
        # Agent C processes Agent B's output
        print("\nAgent C processing...")
        prompt_c = f"Analyze this data from Agent B and prepare summary for Agent A: {result_b.output}"
        result_c = await agent_c.run(prompt_c)
        print(f"Agent C result: {result_c.output}")
        
        # Prepare data for next cycle (C -> A handoff)
        current_data = {
            "task": "Continue processing based on analysis",
            "previous_analysis": str(result_c.output),
        }
    
# Tool example for agents
@agent_a.tool_plain
async def fetch_external_data(query: str) -> Dict[str, Any]:
    """Simulate fetching external data"""
    return {
        "query": query,
        "external_data": f"Mock data for: {query}",
        "timestamp": "2025-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    # Run the agent cycle
    asyncio.run(run_agent_cycle())