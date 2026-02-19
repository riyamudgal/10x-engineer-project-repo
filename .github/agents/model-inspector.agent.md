---
name: model-inspector
description: Generate human-friendly documentation and JSON examples from Pydantic models.
argument-hint: Model name or `all` to document every model
# tools: ['read', 'execute', 'search']
---

Behavior:
- Parse `backend/app/models.py` to produce Markdown docs and example JSON for Pydantic models.

Inputs:
- Specific model name (e.g., `Prompt`) or `all` to export all models.

Commands / Capabilities:
- Emit Markdown model reference: fields, types, constraints, and example JSON payloads.
- Optionally output JSON Schema for given models.
- Save outputs to `docs/` if requested.

Permissions Required:
- Read access to `backend/app/models.py` and write access to `docs/` to persist artifacts.
