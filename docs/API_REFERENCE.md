# PromptLab API Reference

This document describes all HTTP endpoints implemented in backend/app/api.py.

Notes:
- All timestamp fields are ISO 8601 datetimes (UTC).
- Validation errors from FastAPI/Pydantic produce HTTP 422 responses.

---

## Health Check

- Method & Path: GET /health
- Description: Returns API health and version.
- Parameters: none
- Request body: none
- Response format (200):
  - status: string (e.g., "healthy")
  - version: string
- Example response (200):

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

- Error codes:
  - 500: server error

---

## Root

- Method & Path: GET /
- Description: Simple message confirming API is running.
- Parameters: none
- Request body: none
- Response format (200):
  - message: string
- Example response (200):

```json
{
  "message": "PromptLab API is running"
}
```

- Error codes: none specified

---

## Prompts

### List Prompts
- Method & Path: GET /prompts
- Description: Returns a list of prompts, optionally filtered by collection and/or search text, sorted newest-first.
- Parameters (query):
  - collection_id (optional, string): filter prompts by collection id
  - search (optional, string): text to search in prompt title/content/description
- Request body: none
- Response format (200): PromptList
  - prompts: array of Prompt objects
  - total: integer
- Example response (200):

```json
{
  "prompts": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Summarize article",
      "content": "Summarize the following article in 3 sentences...",
      "description": "Short summarization prompt",
      "collection_id": "abcde-collection-1",
      "created_at": "2026-02-19T12:00:00Z",
      "updated_at": "2026-02-19T12:00:00Z"
    }
  ],
  "total": 1
}
```

Prompt (object fields):
- id: string (UUID)
- title: string
- content: string
- description: string | null
- collection_id: string | null
- created_at: datetime (ISO 8601 UTC)
- updated_at: datetime (ISO 8601 UTC)

- Error codes:
  - 422: validation error for query parameters
  - 500: server error


### Get Prompt
- Method & Path: GET /prompts/{prompt_id}
- Description: Retrieve a single prompt by id.
- Parameters (path):
  - prompt_id (required, string)
- Request body: none
- Response format (200): Prompt (see fields above)
- Example response (200):

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Summarize article",
  "content": "Summarize the following article in 3 sentences...",
  "description": "Short summarization prompt",
  "collection_id": "abcde-collection-1",
  "created_at": "2026-02-19T12:00:00Z",
  "updated_at": "2026-02-19T12:00:00Z"
}
```

- Error codes:
  - 404: Prompt not found
  - 422: invalid prompt_id format
  - 500: server error


### Create Prompt
- Method & Path: POST /prompts
- Description: Create a new prompt.
- Parameters: none
- Request body (application/json): PromptCreate
  - title: string (required, 1-200 chars)
  - content: string (required)
  - description: string | null (optional, max 500 chars)
  - collection_id: string | null (optional)
- Response format (201): Prompt (full object with generated id, created_at, updated_at)
- Example request body:

```json
{
  "title": "Summarize article",
  "content": "Summarize the following article in 3 sentences...",
  "description": "Short summarization prompt",
  "collection_id": "abcde-collection-1"
}
```

- Example response (201):

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Summarize article",
  "content": "Summarize the following article in 3 sentences...",
  "description": "Short summarization prompt",
  "collection_id": "abcde-collection-1",
  "created_at": "2026-02-19T12:00:00Z",
  "updated_at": "2026-02-19T12:00:00Z"
}
```

- Error codes:
  - 400: Referenced collection not found
  - 422: validation error (missing/invalid fields)
  - 500: server error


### Update Prompt (full)
- Method & Path: PUT /prompts/{prompt_id}
- Description: Replace an existing prompt with provided data (updates updated_at).
- Parameters (path):
  - prompt_id (required, string)
- Request body (application/json): PromptUpdate (same fields as PromptCreate)
- Response format (200): Prompt (the updated prompt)
- Example request body:

```json
{
  "title": "Summarize article (updated)",
  "content": "Updated content...",
  "description": "Updated description",
  "collection_id": "abcde-collection-1"
}
```

- Example response (200):

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Summarize article (updated)",
  "content": "Updated content...",
  "description": "Updated description",
  "collection_id": "abcde-collection-1",
  "created_at": "2026-02-19T12:00:00Z",
  "updated_at": "2026-02-19T12:30:00Z"
}
```

- Error codes:
  - 404: Prompt not found
  - 400: Referenced collection not found
  - 422: validation error
  - 500: server error


### Patch Prompt (partial)
- Method & Path: PATCH /prompts/{prompt_id}
- Description: Partial update — only provided fields are changed (updates updated_at).
- Parameters (path):
  - prompt_id (required, string)
- Request body (application/json): PromptUpdate (fields may be omitted to leave unchanged)
- Response format (200): Prompt (the updated prompt)
- Example request body (partial):

```json
{
  "description": "New short description"
}
```

- Example response (200):

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Summarize article",
  "content": "Summarize the following article in 3 sentences...",
  "description": "New short description",
  "collection_id": "abcde-collection-1",
  "created_at": "2026-02-19T12:00:00Z",
  "updated_at": "2026-02-19T12:45:00Z"
}
```

- Error codes:
  - 404: Prompt not found
  - 400: Referenced collection not found
  - 422: validation error
  - 500: server error


### Delete Prompt
- Method & Path: DELETE /prompts/{prompt_id}
- Description: Delete a prompt by id.
- Parameters (path):
  - prompt_id (required, string)
- Request body: none
- Response format: 204 No Content (empty body)
- Example error response (404):

```json
{
  "detail": "Prompt not found"
}
```

- Error codes:
  - 404: Prompt not found
  - 500: server error

---

## Collections

### List Collections
- Method & Path: GET /collections
- Description: Returns all collections.
- Parameters: none
- Request body: none
- Response format (200): CollectionList
  - collections: array of Collection objects
  - total: integer
- Example response (200):

```json
{
  "collections": [
    {
      "id": "abcde-collection-1",
      "name": "Summaries",
      "description": "Prompts used for generating summaries",
      "created_at": "2026-02-19T11:50:00Z"
    }
  ],
  "total": 1
}
```

Collection (object fields):
- id: string (UUID)
- name: string
- description: string | null
- created_at: datetime (ISO 8601 UTC)

- Error codes:
  - 500: server error


### Get Collection
- Method & Path: GET /collections/{collection_id}
- Description: Retrieve a single collection by id.
- Parameters (path):
  - collection_id (required, string)
- Request body: none
- Response format (200): Collection (see fields above)
- Example response (200):

```json
{
  "id": "abcde-collection-1",
  "name": "Summaries",
  "description": "Prompts used for generating summaries",
  "created_at": "2026-02-19T11:50:00Z"
}
```

- Error codes:
  - 404: Collection not found
  - 422: invalid collection_id format
  - 500: server error


### Create Collection
- Method & Path: POST /collections
- Description: Create a new collection.
- Parameters: none
- Request body (application/json): CollectionCreate
  - name: string (required, 1-100 chars)
  - description: string | null (optional, max 500 chars)
- Response format (201): Collection (with generated id and created_at)
- Example request body:

```json
{
  "name": "Summaries",
  "description": "Prompts used for generating summaries"
}
```

- Example response (201):

```json
{
  "id": "abcde-collection-1",
  "name": "Summaries",
  "description": "Prompts used for generating summaries",
  "created_at": "2026-02-19T11:50:00Z"
}
```

- Error codes:
  - 422: validation error
  - 500: server error


### Delete Collection
- Method & Path: DELETE /collections/{collection_id}
- Description: Delete a collection and attempt to remove references from prompts (prompts' collection_id set to null).
- Parameters (path):
  - collection_id (required, string)
- Request body: none
- Response format: 204 No Content (empty body)
- Example error response (404):

```json
{
  "detail": "Collection not found"
}
```

- Error codes:
  - 404: Collection not found
  - 500: Failed to delete collection or server error

---

## Common Responses & Errors
- 200: OK — successful GET/PUT/PATCH responses return model objects as documented.
- 201: Created — successful POST returns the created resource.
- 204: No Content — successful DELETE returns no body.
- 400: Bad Request — used when a referenced collection does not exist in create/update operations.
- 404: Not Found — resource with specified id does not exist.
- 422: Unprocessable Entity — request body or parameters failed Pydantic validation.
- 500: Internal Server Error — unexpected server error.

---
