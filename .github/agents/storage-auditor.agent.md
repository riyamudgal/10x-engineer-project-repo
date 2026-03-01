---
name: storage-auditor
description: Inspect in-memory storage state and run integrity checks for prompts/collections.
argument-hint: Action (e.g., "list", "audit", "simulate-delete <id>")
# tools: ['read', 'execute']
---

Behavior:
- Interact with the `storage` object to list items and run integrity checks.
- Detect orphaned prompts, duplicate IDs, and simulate collection deletions.

Inputs:
- Commands: `list`, `audit`, `simulate-delete <collection_id>`, `clear`.

Commands / Capabilities:
- Return current storage contents summary and counts.
- Run audits (orphaned prompts, missing referenced collections).
- Simulate deletion cascade and show affected prompts without mutating state unless requested.

Permissions Required:
- Read access to `backend/app/storage.py` and ability to import/run small Python helpers in the workspace.
