
# Prompt Versions Specification

## Overview & Motivation
Prompt versioning provides **audit history**, **safe rollback**, and **change tracking**
for prompts stored in PromptLab’s in-memory `Storage`.

Each create or update operation records an immutable snapshot of the prompt,
allowing developers to inspect or restore previous states without introducing
database migrations or a full version-control system.

This design intentionally mirrors the simplicity of `storage.py`.

## Goals & Non-goals

### Goals
- Track all prompt changes (create, update, patch, revert)
- Enable rollback to any previous state
- Use full prompt snapshots (simple and reliable)
- Require minimal changes to existing storage logic

### Non-goals
- Branching or merging versions
- Delta/diff-based storage
- Persistent storage guarantees
- Background jobs or async processing

## Data Model

### PromptVersion
| Field | Type | Description |
|---|---|---|
| id | str | Unique version identifier |
| prompt_id | str | ID of the prompt |
| version_number | int | Starts at 1, increments per prompt |
| snapshot | Prompt | Immutable copy of the prompt |
| change_summary | str? | Optional human-readable description |
| created_at | str | ISO-8601 timestamp |

### Version Semantics
- Version **1** is created in `Storage.create_prompt`
- Any call to `update_prompt` creates a new version
- Reverting creates a **new version**, not overwrite history

### Example
```json
{
  "id": "pv_002",
  "prompt_id": "p1",
  "version_number": 2,
  "snapshot": {
    "id": "p1",
    "title": "Summarize",
    "content": "Summarize the input text",
    "description": null,
    "collection_id": "c1",
    "created_at": "2026-02-19T08:00:00Z",
    "updated_at": "2026-02-19T08:10:00Z"
  },
  "change_summary": "Updated wording",
  "created_at": "2026-02-19T08:10:00Z"
}
