"""FastAPI routes for PromptLab.

This module registers HTTP routes for the PromptLab API. Each route
handler includes a Google-style docstring describing arguments,
return values and an example usage. The handlers are designed to be
used by FastAPI; examples show direct function invocation for
clarity during testing.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return basic health information for the API.

    Returns:
        HealthResponse: Object containing `status` (e.g. "healthy") and
            `version` (API version string).

    Example:
        >>> health_check()
        HealthResponse(status='healthy', version='0.1.0')
    """

    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """List prompts, optionally filtered by collection or search text.

    Args:
        collection_id (Optional[str]): If provided, only prompts belonging
            to this collection id are returned.
        search (Optional[str]): If provided, prompts are filtered by a
            full-text search across title/content/description.

    Returns:
        PromptList: An object with `prompts` (list of `Prompt`) and
            `total` (int) representing the count of returned prompts.

    Example:
        >>> list_prompts(collection_id='abc', search='summarize')
        PromptList(prompts=[Prompt(... )], total=1)
    """

    prompts = storage.get_all_prompts()
    
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a single prompt by id.

    Args:
        prompt_id (str): The UUID or identifier of the prompt to retrieve.

    Returns:
        Prompt: The requested prompt object.

    Raises:
        HTTPException: 404 if the prompt does not exist.

    Example:
        >>> get_prompt('123e4567-e89b-12d3-a456-426614174000')
        Prompt(id='123e4567-e89b-12d3-a456-426614174000', title='...')
    """

    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.get("/")
def root():
    """Root endpoint returning a simple status message.

    Returns:
        dict: A JSON-serializable dict with a `message` describing the API.

    Example:
        >>> root()
        {"message": "PromptLab API is running"}
    """

    return {"message": "PromptLab API is running"}


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.

    Args:
        prompt_data (PromptCreate): Request body containing the prompt
            fields: `title` (str), `content` (str), optional
            `description` (str) and optional `collection_id` (str).

    Returns:
        Prompt: The created Prompt including generated `id`, `created_at`
            and `updated_at` timestamps.

    Raises:
        HTTPException: 400 if `collection_id` is provided but the
            referenced collection does not exist.

    Example:
        >>> create_prompt(PromptCreate(title='Summarize', content='...'))
        Prompt(id='1234', title='Summarize', ...)
    """

    # Ensure referenced collection exists
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Replace an existing prompt with new data (full update).

    Args:
        prompt_id (str): Identifier of the prompt to update.
        prompt_data (PromptUpdate): New prompt data (all fields expected).

    Returns:
        Prompt: The updated prompt object with refreshed `updated_at`.

    Raises:
        HTTPException: 404 if the prompt does not exist;
            400 if provided `collection_id` does not exist.

    Example:
        >>> update_prompt('1234', PromptUpdate(title='New', content='...'))
        Prompt(id='1234', title='New', ...)
    """

    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Full update with timestamp refresh
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Partially update a prompt; only provided fields are changed.

    Args:
        prompt_id (str): Identifier of the prompt to patch.
        prompt_data (PromptUpdate): Fields to update. Any field set to
            ``None`` will be left unchanged.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: 404 if the prompt does not exist;
            400 if provided `collection_id` does not exist.

    Example:
        >>> patch_prompt('1234', PromptUpdate(description='Short desc'))
        Prompt(id='1234', description='Short desc', ...)
    """

    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Partial update - only update fields that are provided
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title if prompt_data.title is not None else existing.title,
        content=prompt_data.content if prompt_data.content is not None else existing.content,
        description=prompt_data.description if prompt_data.description is not None else existing.description,
        collection_id=prompt_data.collection_id if prompt_data.collection_id is not None else existing.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by id.

    Args:
        prompt_id (str): Identifier of the prompt to delete.

    Returns:
        None: On success returns HTTP 204 No Content.

    Raises:
        HTTPException: 404 if the prompt does not exist.

    Example:
        >>> delete_prompt('1234')  # returns None (204)
        None
    """

    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """Return all collections.

    Returns:
        CollectionList: Object with `collections` (list of `Collection`)
            and `total` (int).

    Example:
        >>> list_collections()
        CollectionList(collections=[Collection(... )], total=1)
    """

    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a collection by id.

    Args:
        collection_id (str): Identifier of the collection to retrieve.

    Returns:
        Collection: The requested collection object.

    Raises:
        HTTPException: 404 if the collection does not exist.

    Example:
        >>> get_collection('abcde-collection-1')
        Collection(id='abcde-collection-1', name='Summaries', ...)
    """

    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    Args:
        collection_data (CollectionCreate): Request body with `name`
            (str) and optional `description` (str).

    Returns:
        Collection: The created collection including generated `id`
            and `created_at`.

    Example:
        >>> create_collection(CollectionCreate(name='Summaries'))
        Collection(id='abcde-collection-1', name='Summaries', ...)
    """

    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection and remove references from prompts.

    This endpoint deletes the collection identified by ``collection_id``.
    After deletion, any prompts that referenced the collection will have
    their ``collection_id`` set to ``None``. Deletion is idempotent in the
    sense that a missing collection results in a 404.

    Args:
        collection_id (str): Identifier of the collection to delete.

    Returns:
        None: On success returns HTTP 204 No Content.

    Raises:
        HTTPException: 404 if the collection does not exist; 500 if the
            underlying storage failed to delete the collection.

    Example:
        >>> delete_collection('abcde-collection-1')  # returns None (204)
        None
    """

    # Verify collection exists before deletion
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Perform deletion
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=500, detail="Failed to delete collection")

    # Clean up prompts that reference this collection
    try:
        all_prompts = storage.get_all_prompts()
        for prompt in all_prompts:
            if prompt.collection_id == collection_id:
                prompt.collection_id = None
                storage.update_prompt(prompt.id, prompt)
    except Exception as e:
        # Log but don't fail - deletion already succeeded
        print(f"Warning: Failed to cleanup orphaned prompts: {e}")

    return None
