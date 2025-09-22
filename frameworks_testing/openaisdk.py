# Issues: sometimes doesn't hand off and sometimes doesn't produce output that is asked.
# Overall do not recommend as there is no way to ensure transfer without building our own graph-like structure.
# Even if we do this, the lack of ability to consistently give structured output makes this inviable.
# Maybe some improvements on the handoff tool calls could be helpful (descriptions, etc.)

from agents import Agent, Runner, RunConfig, function_tool
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- Define tools ---
user_info = "The name of the user is Nehan. Nehan has six dogs and three cats. Nehan's favorite color is green."
@function_tool
def update_user_info(newinfo: str) -> None:
    global user_info
    user_info += " " + newinfo

@function_tool
def get_user_info() -> str:
    """Gets a string with information about the user."""
    return user_info

# --- Define structured output ---
class UserInformation(BaseModel):
    name: str
    num_dogs: int
    num_cats: int
    favorite_color: str
    other_details: str

class AnalyzerOutput(BaseModel):
    new_detail: str

# --- Agent A: Retriever ---
agent_A = Agent(
    name="Retriever",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a retriever agent. Retrieve the user's information using the get_user_info tool,
parse it into structured JSON (UserInformation), and hand it to the Analyzer agent.
""",
    model="gpt-4.1-mini",
    tools=[get_user_info],
    handoffs=[],  # will set later
    output_type=UserInformation,
)

# --- Agent B: Analyzer ---
agent_B = Agent(
    name="Analyzer",
    instructions=RECOMMENDED_PROMPT_PREFIX + """
You are an analysis agent. You receive structured JSON about the user.
You MUST produce exactly JSON in the following format:

{"new_detail": "<a NEW fictitious detail about the user. Ensure that it is not any information already given and that it's NEW.>"}

ALWAYS hand off the JSON to the Reporter agent.
""",
    model="gpt-4.1-mini",
    tools=[],
    handoffs=[],  # will set later
    output_type=AnalyzerOutput,
)

# --- Agent C: Reporter ---
agent_C = Agent(
    name="Reporter",
    instructions=RECOMMENDED_PROMPT_PREFIX + """
You are a reporting agent. You receive Analyzer's structured JSON {"new_detail": "..."}.
There are one of two cases:
1. If there is any new information from the Analyzer that isn't already in the user info (which can be obtained via the get_user_info tool), then
update the user's information using update_user_info tool, then hand off back to Retriever to continue the cycle.
2. Otherwise, simply end the cycle and do not hand off to another agent or update the user info.
""",
    model="gpt-4.1-mini",
    tools=[get_user_info, update_user_info],
    handoffs=[],  # will set later
)
agent_A.handoffs = [agent_B]
agent_B.handoffs = [agent_C]
agent_C.handoffs = [agent_A]

if __name__ == "__main__":
    initial_input = "Hello from user: start the cycle"

    run_config = RunConfig(workflow_name="ThreeAgentCycle")
    result = Runner.run_sync(starting_agent=agent_A, input=initial_input, run_config=run_config, max_turns=6)
    print(result.to_input_list())
    print("Final Output: ", result.final_output)
    print("UserInfo: " + user_info)