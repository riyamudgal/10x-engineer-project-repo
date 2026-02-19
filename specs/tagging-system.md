
---

## 📄 `specs/tagging-system.md`

```md
# Tagging System Specification

## Overview & Motivation
The tagging system enables **flexible categorization**, **filtering**, and **bulk operations** on prompts without introducing hierarchical complexity.

Tags are implemented as **first-class objects**, while prompts maintain references via `tag_ids`, aligning with PromptLab’s in-memory storage design.

## Goals & Non-goals

### Goals
- Assign multiple tags to prompts
- Filter prompts by tag
- Lightweight metadata (color, description)
- Minimal impact on existing prompt routes

### Non-goals
- Nested or hierarchical tags
- Automatic tag inference
- Role-based permissions

## Data Model

### Tag
| Field | Type | Description |
|---|---|---|
| id | string | Unique identifier |
| name | string | Unique, case-insensitive |
| description | string? | Optional |
| color | string? | Optional hex color |

### Prompt Extension
```python
tag_ids: list[str]

