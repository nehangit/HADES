import os

# Absolute path to the directory containing config.py (your project root)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Path to agent_workspace inside the root
SANDBOX_ROOT = os.path.join(PROJECT_ROOT, "agent_workspace")

# Create the workspace folder if it doesn't exist
os.makedirs(SANDBOX_ROOT, exist_ok=True)