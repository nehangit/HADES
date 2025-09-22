# Dont recommend as the crews have bad multi agent design patterns and the flows are unnecessarily difficult to work with especially
# for loops.
# Current code is broken. Not sure how to properly fix loops/etc.

from crewai import Agent
from crewai.tools import tool
from crewai.flow.flow import Flow, start, listen
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- A tool for Agent A ---
@tool("fetch_news_data")
async def fetch_news_data() -> List[Dict[str, str]]:
    """Get recent news articles about the company"""
    return [
        {
            "title": "Tesla Expands Cybertruck Production",
            "date": "2024-03-20",
            "summary": "Tesla ramps up Cybertruck manufacturing capacity at Gigafactory Texas, aiming to meet strong demand.",
        },
        {
            "title": "Tesla FSD Beta Shows Promise",
            "date": "2024-03-19",
            "summary": "Latest Full Self-Driving beta demonstrates significant improvements in urban navigation and safety features.",
        },
        {
            "title": "Model Y Dominates Global EV Sales",
            "date": "2024-03-18",
            "summary": "Tesla's Model Y becomes best-selling electric vehicle worldwide, capturing significant market share.",
        },
    ]

# --- Agents ---
agent_a = Agent(
    name="Agent A",
    role="Data Collector",
    goal="Collect initial data and send to Agent B",
    backstory="You gather raw information and enrich it with external data.",
    tools=[fetch_news_data],  # attach the tool
)

agent_b = Agent(
    name="Agent B",
    role="Data Processor",
    goal="Process data from Agent A and send to Agent C",
    backstory="You transform and enhance the data for analysis.",
)

agent_c = Agent(
    name="Agent C",
    role="Data Analyzer",
    goal="Analyze processed data from Agent B and send insights back to Agent A",
    backstory="You analyze the data and produce insights.",
)

class ThreeAgentFlow(Flow):

    @start()
    async def collect_data(self):
        """Agent A collects data"""
        self.state['cycles'] = 0
        self.state['input'] = {"task": "Start processing customer feedback"}
        self.state['step_a'] = await agent_a.kickoff_async(
            f"Use your tool if needed. Collect and prepare data for Agent B. Input: {self.state['input']}"
        )

    @listen(collect_data)
    async def process_data(self):
        """Agent B processes data from Agent A"""
        self.state['step_b'] = await agent_b.kickoff_async(
            f"Process data from Agent A and prepare for Agent C. Input: {self.state['step_a']}"
        )

    @listen(process_data)
    async def analyze_data(self):
        """Agent C analyzes data from Agent B"""
        self.state['step_c'] = await agent_c.kickoff_async(
            f"Analyze data from Agent B and send summary back to Agent A. Input: {self.state['step_b']}"
        )

    @listen(analyze_data)
    async def loop_back(self):
        """Loop back to Agent A until max cycles reached"""
        self.state['cycles'] += 1
        if self.state['cycles'] < 2:  # run 2 cycles total
            self.state['input'] = {
                "task": "Continue processing based on previous analysis",
                "previous_analysis": self.state['step_c']
            }
            # restart the cycle by calling collect_data again
            await self.collect_data()
            await self.process_data()
            await self.analyze_data()
            await self.loop_back()
        else:
            print("\nFinal result:", self.state['step_c'])

# --- Run flow ---
flow = ThreeAgentFlow("ThreeAgentCycle")

flow.kickoff()
