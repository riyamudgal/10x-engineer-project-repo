"""Utility helper functions used across PromptLab backend.

This module contains reusable helper functions for prompt processing
such as sorting, filtering, searching, validation, and template parsing.
"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by their creation timestamp.

    This function sorts a list of Prompt objects based on the `created_at`
    field.

    Args:
        prompts (List[Prompt]):
            List of Prompt objects to be sorted.

        descending (bool, optional):
            If True, prompts are sorted from newest to oldest.
            If False, prompts are sorted from oldest to newest.
            Defaults to True.

    Returns:
        List[Prompt]:
            A new list of Prompt objects sorted by creation date.

    Example:
        >>> prompts = [Prompt(id="1", created_at="2024-01-01"), Prompt(id="2", created_at="2024-01-02")]
        >>> sort_prompts_by_date(prompts)
        [Prompt(id='2'), Prompt(id='1')]
    """

    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts that belong to a specific collection.

    Args:
        prompts (List[Prompt]):
            List of Prompt objects to filter.

        collection_id (str):
            ID of the collection whose prompts should be returned.

    Returns:
        List[Prompt]:
            List containing only prompts whose `collection_id`
            matches the provided collection ID.

    Example:
        >>> filter_prompts_by_collection(prompts, "collection-123")
        [Prompt(id='1', collection_id='collection-123')]
    """

    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description.

    Performs a case-insensitive search across prompt titles and descriptions.

    Args:
        prompts (List[Prompt]):
            List of Prompt objects to search.

        query (str):
            Search text used to filter prompts.

    Returns:
        List[Prompt]:
            List of prompts whose `title` or `description`
            contains the search query.

    Example:
        >>> search_prompts(prompts, "summarize")
        [Prompt(title='Summarize article')]
    """

    query_lower = query.lower()
    return [
        p for p in prompts
        if query_lower in p.title.lower()
        or (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Validate the content of a prompt.

    A prompt is considered valid if:
    - It is not empty
    - It is not only whitespace
    - It contains at least 10 characters after trimming

    Args:
        content (str):
            Prompt text content to validate.

    Returns:
        bool:
            True if the prompt content is valid, otherwise False.

    Example:
        >>> validate_prompt_content("Summarize the following text")
        True

        >>> validate_prompt_content("   ")
        False
    """

    if not content or not content.strip():
        return False

    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.

    Variables are defined using the format:

    {{variable_name}}

    This function scans the prompt content and extracts all variable
    placeholders.

    Args:
        content (str):
            Prompt content containing template variables.

    Returns:
        List[str]:
            List of extracted variable names.

    Example:
        >>> extract_variables("Write about {{topic}} in {{language}}")
        ['topic', 'language']
    """

    import re

    pattern = r"\{\{(\w+)\}\}"
    return re.findall(pattern, content)