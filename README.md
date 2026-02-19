<<<<<<< HEAD
=======
# PromptLab

PromptLab is a small in-memory AI prompt engineering platform exposing
a simple HTTP API for creating, updating, searching, and organizing
prompts into collections. It is intended as an educational project and
for local development and testing; persistent storage is not provided.

## Project Overview

- Simple FastAPI application providing REST endpoints for prompts and
	collections.
- Pydantic models enforce validation and shape of request/response data.
- In-memory storage (see `backend/app/storage.py`) makes it easy to run
	locally and reset state between tests.

## Requirements

- Python 3.10+
- See `backend/requirements.txt` for exact pinned packages.

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

## Run the API (development)

From the `backend/` directory run:

```bash
python main.py
```

The API will be available at http://127.0.0.1:8000

FastAPI interactive docs are at http://127.0.0.1:8000/docs

## API Endpoints

All endpoints are under the root server (no prefix). Key endpoints:

- GET `/` — Root: returns a simple status message.
- GET `/health` — Health check; returns `status` and `version`.

Prompts
- GET `/prompts` — List prompts. Optional query params:
	- `collection_id` (str) — filter by collection id
	- `search` (str) — full-text search across title/content/description
	Returns: `PromptList` (prompts, total)
- GET `/prompts/{prompt_id}` — Retrieve a single prompt by id.
- POST `/prompts` — Create a new prompt.
	Body: `PromptCreate` (title, content, optional description, optional collection_id)
- PUT `/prompts/{prompt_id}` — Full replace update for a prompt.
- PATCH `/prompts/{prompt_id}` — Partial update (only provided fields changed).
- DELETE `/prompts/{prompt_id}` — Delete a prompt (204 No Content).

Collections
- GET `/collections` — List collections. Returns `CollectionList`.
- GET `/collections/{collection_id}` — Retrieve a collection by id.
- POST `/collections` — Create a collection. Body: `CollectionCreate` (name, optional description)
- DELETE `/collections/{collection_id}` — Delete a collection; prompts referencing it will have their `collection_id` cleared.

## Data Models

Models are defined in `backend/app/models.py` using Pydantic.

- `PromptBase`:
	- `title` (str): 1-200 chars
	- `content` (str)
	- `description` (Optional[str])
	- `collection_id` (Optional[str])
- `PromptCreate` / `PromptUpdate` — request models for creating/updating prompts.
- `Prompt` (response model): extends `PromptBase` with
	- `id` (str, UUID4)
	- `created_at` (datetime UTC)
	- `updated_at` (datetime UTC)

- `CollectionBase`:
	- `name` (str): 1-100 chars
	- `description` (Optional[str])
- `CollectionCreate` — request model for creating collections.
- `Collection` (response model): extends `CollectionBase` with
	- `id` (str, UUID4)
	- `created_at` (datetime UTC)

- `PromptList` / `CollectionList` — wrapper response models with `items` and `total` counts.
- `HealthResponse` — `{status: str, version: str}`

## Usage Examples

Create a collection (curl):

```bash
curl -X POST http://127.0.0.1:8000/collections \
	-H "Content-Type: application/json" \
	-d '{"name": "Summaries", "description": "Short summary prompts"}'
```

Create a prompt (curl):

```bash
curl -X POST http://127.0.0.1:8000/prompts \
	-H "Content-Type: application/json" \
	-d '{"title": "Summarize", "content": "Summarize this article in 3 bullets.", "collection_id": "<id>"}'
```

List prompts (with optional query):

```bash
curl "http://127.0.0.1:8000/prompts?collection_id=<id>&search=summarize"
```

Python example using `httpx`:

```python
import httpx

client = httpx.Client(base_url="http://127.0.0.1:8000")

# Create collection
resp = client.post("/collections", json={"name": "Examples"})
collection = resp.json()

# Create prompt
resp = client.post("/prompts", json={"title": "Greet", "content": "Say hello to the user", "collection_id": collection['id']})
prompt = resp.json()

print(prompt)
```

## Testing

Run the test suite from the `backend/` directory:

```bash
pytest -q
```

## Notes & Next Steps

- Storage is in-memory and not shared across processes. For production,
	add a database-backed storage layer.
- Authentication/authorization is not implemented.
- Consider pagination for `/prompts` when the dataset grows.

## License

This repository is provided for educational purposes.
>>>>>>> b180b0a8ba055a6c740fe186edff9575ab58843c
