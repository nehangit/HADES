# Hierarchical Agent Driven Exploitation System (HADES)

⚠️ DISCLAIMER

This project is intended strictly for use in **controlled environments** such as penetration testing labs, Capture The Flag (CTF) platforms, or legally authorized security research.

**Do not use this software against any system or target without proper authorization.**

The authors and contributors are not responsible for any misuse or damage caused by this tool. Use of this project is entirely at your own risk.

By using this tool, you agree to comply with all applicable laws and ethical guidelines in your jurisdiction.

## Overview

Based on HPTSA: https://arxiv.org/pdf/2406.01637

A hierarchical multi-agent based autonomous system for web vulnerability recon and exploitation. It consists of:

- A hierarchical planner for environment exploration and task planning
- A team manager for orchestrating task-specific agents
- A set of expert agents (SQLi, XSS, CSRF, SSTI, ZAP, Generic) for exploiting specific web vulnerabilities

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
