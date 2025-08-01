# Hierarchical Agent-Based Exploitation System (HABES)

## Overview

Based on HPTSA: https://arxiv.org/pdf/2406.01637

A hierarchical multi-agent based autonomous system for web vulnerability recon and exploitation. It consists of:

- A hierarchical planner for environment exploration and task planning
- A team manager for orchestrating task-specific agents
- A set of expert agents (SQLi, XSS, CSRF, SSTI, ZAP, Generic) for exploiting specific vulnerabilities

## Components

- `planner/` — Hierarchical planner logic
- `manager/` — Team manager for agents
- `agents/` — Task-specific expert agents
- `tools/` — Wrappers for Playwright, terminal, file management, ZAP, sqlmap
- `utils/` — HTML simplification and shared utilities
- `main.py` — Entry point

## Setup

1. Install dependencies (in a virtual environment):
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
2. Set up your API keys for OpenAI and Fireworks in a `.env` file:
   ```env
   OPENAI_API_KEY=your-key
   FIREWORKS_API_KEY=your-key
   ```
3. Run the system:
   ```bash
   python main.py
   ```

## Notes

- zap.sh and sqlmap must be installed and available in your PATH for their respective agents
