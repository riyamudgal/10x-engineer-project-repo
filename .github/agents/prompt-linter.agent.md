---
name: prompt-linter
description: Lint and evaluate prompt quality using repo utilities and heuristics.
argument-hint: Path or `all` to lint all stored prompts
# tools: ['read', 'execute', 'search']
---

Behavior:
- Use `validate_prompt_content` and `extract_variables` to flag issues and suggestions.

Inputs:
- A prompt id, file path, or `all` to run across storage.

Commands / Capabilities:
- Report invalid/short prompts, unused or missing variables, and formatting issues.
- Provide rewrite suggestions and severity levels (error/warning/info).
- Produce batch report (CSV/JSON) for review.

Permissions Required:
- Read access to `backend/app/utils.py` and `backend/app/storage.py` for live checks.
