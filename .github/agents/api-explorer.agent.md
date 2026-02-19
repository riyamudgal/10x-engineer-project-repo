---
name: api-explorer
description: Discover, exercise and validate the PromptLab HTTP API endpoints.
argument-hint: Endpoint or test plan (e.g., "GET /prompts" or a list of endpoints to probe).
# tools: ['http', 'read', 'execute', 'search']
---

Behavior:
- Inspect route definitions (backend/app/api.py) or OpenAPI and enumerate endpoints.
- Execute example requests and return status, headers, and parsed JSON.

Inputs:
- A single endpoint (method + path) or array of endpoints.
- Optional JSON payload and query parameters.

Commands / Capabilities:
- List available endpoints and required request shapes.
- Make requests against a running server (default: http://localhost:8000).
- Validate responses against Pydantic models and report mismatches.
- Emit reproducible curl/HTTPie examples and brief troubleshooting hints.

Permissions Required:
- Network: ability to call local dev server (http://localhost:8000).
- Read access to `backend/app/api.py` and `backend/app/models.py` for schema inference.
