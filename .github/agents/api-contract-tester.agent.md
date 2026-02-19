---
name: api-contract-tester
description: Enforce that runtime API responses match the declared Pydantic response models.
argument-hint: Endpoint(s) to test or `all`
# tools: ['http', 'read', 'execute']
---

Behavior:
- Call endpoints and validate responses against models in `backend/app/models.py`.

Inputs:
- Single endpoint, list of endpoints, or `all` to test all documented routes.

Commands / Capabilities:
- Run requests, deserialize into Pydantic models and surface validation errors.
- Produce a report listing mismatches, offending fields, and example failing payloads.

Permissions Required:
- Network access to the dev server and read access to model definitions.
