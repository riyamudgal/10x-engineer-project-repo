"""Pydantic models for PromptLab.

This module defines the data models used by the PromptLab API. Models
are implemented with Pydantic and include helpful validation. The
docstrings for each model follow the Google style and describe fields
and example usage.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a random UUID string.

    Returns:
        str: A UUID4 string used as an identifier for models.

    Example:
        >>> generate_id()
        '123e4567-e89b-12d3-a456-426614174000'
    """

    return str(uuid4())


def get_current_time() -> datetime:
    """Return the current UTC datetime.

    Returns:
        datetime: Current UTC timestamp (naive datetime in UTC).

    Example:
        >>> isinstance(get_current_time(), datetime)
        True
    """

    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base fields for a Prompt.

    Fields:
        title (str): Human-readable title for the prompt. Required. 1-200 chars.
        content (str): The prompt text or instructions. Required.
        description (Optional[str]): Optional short description (max 500 chars).
        collection_id (Optional[str]): Optional id of the parent collection.

    Example:
        >>> PromptBase(
        ...     title="Summarize article",
        ...     content="Summarize in 3 sentences",
        ...     description="Short summary prompt",
        ...     collection_id="collection-123"
        ... )
    """

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Model used when creating a new Prompt.

    Inherits all fields from :class:`PromptBase` and is used as the
    request body for POST /prompts.
    """


class PromptUpdate(PromptBase):
    """Model used when updating an existing Prompt.

    The same fields as :class:`PromptBase` are accepted. For PATCH
    operations, fields may be omitted to leave them unchanged.
    """


class Prompt(PromptBase):
    """Full Prompt model returned by the API.

    Fields (in addition to PromptBase):
        id (str): Unique identifier (UUID4 string) generated server-side.
        created_at (datetime): Timestamp when the prompt was created (UTC).
        updated_at (datetime): Timestamp when the prompt was last updated (UTC).

    Example (constructed by server):
        >>> Prompt(
        ...     id="123e4567-e89b-12d3-a456-426614174000",
        ...     title="Summarize article",
        ...     content="Summarize in 3 sentences",
        ...     description="Short summary",
        ...     collection_id=None,
        ...     created_at=get_current_time(),
        ...     updated_at=get_current_time()
        ... )
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base fields for a Collection.

    Fields:
        name (str): Collection name. Required. 1-100 chars.
        description (Optional[str]): Optional description (max 500 chars).

    Example:
        >>> CollectionBase(name="Summaries", description="For summary prompts")
    """

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model used when creating a new Collection.

    Inherits from :class:`CollectionBase` and is used as the request body
    for POST /collections.
    """


class Collection(CollectionBase):
    """Full Collection model returned by the API.

    Fields (in addition to CollectionBase):
        id (str): Unique identifier (UUID4 string).
        created_at (datetime): Creation timestamp (UTC).

    Example:
        >>> Collection(
        ...     id="abcde-collection-1",
        ...     name="Summaries",
        ...     description="Prompts used for generating summaries",
        ...     created_at=get_current_time()
        ... )
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Paginated list of prompts returned by GET /prompts.

    Fields:
        prompts (List[Prompt]): List of Prompt objects.
        total (int): Total number of prompts in the list.

    Example:
        >>> PromptList(prompts=[Prompt(... )], total=1)
    """

    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """List of collections returned by GET /collections.

    Fields:
        collections (List[Collection]): List of Collection objects.
        total (int): Total number of collections.

    Example:
        >>> CollectionList(collections=[Collection(... )], total=1)
    """

    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Health check response model.

    Fields:
        status (str): Health status, e.g. "healthy".
        version (str): API version string.

    Example:
        >>> HealthResponse(status="healthy", version="0.1.0")
    """

    status: str
    version: str
