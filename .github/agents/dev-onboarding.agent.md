---
name: dev-onboarding
description: Provide reproducible dev environment setup and quick-start steps.
argument-hint: Action (e.g., "setup", "start-server", "run-tests")
# tools: ['execute', 'read']
---

Behavior:
- Produce step-by-step environment setup, venv commands, and smoke checks.

Inputs:
- Commands: `setup`, `start-server`, `run-tests`.

Commands / Capabilities:
- Create recommended virtualenv commands and `pip install -r backend/requirements.txt` steps.
- Provide exact commands to start the server (`python backend/main.py`) and run tests (`pytest`).
- Optionally run quick health-check requests to verify the running server.

Permissions Required:
- Execute shell commands for setup and tests; read access to `backend/requirements.txt` and README.
