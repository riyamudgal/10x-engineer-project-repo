"""In-memory storage for PromptLab.

This module provides a lightweight in-memory store for `Prompt` and
`Collection` objects used by the application. It is intended for tests
and local development; a production deployment would replace this module
with a database-backed implementation.

Module-level globals
    storage (Storage): A single global instance of :class:`Storage`
        used by the rest of the application.

Example:
    >>> from app.storage import storage
    >>> from app.models import Prompt, Collection
    >>> col = Collection(id="c1", name="Examples")
    >>> storage.create_collection(col)
    >>> p = Prompt(id="p1", text="Say hello", collection_id="c1")
    >>> storage.create_prompt(p)
    >>> storage.get_prompt("p1")
    <Prompt id=p1 ...>
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """In-memory storage container for prompts and collections.

    This class keeps two private dictionaries:

    Attributes:
        _prompts (Dict[str, Prompt]): Mapping of prompt id -> :class:`Prompt`.
        _collections (Dict[str, Collection]): Mapping of collection id -> :class:`Collection`.

    Example:
        >>> from app.models import Prompt, Collection
        >>> s = Storage()
        >>> c = Collection(id="c1", name="Examples")
        >>> s.create_collection(c)
        >>> p = Prompt(id="p1", text="Test", collection_id="c1")
        >>> s.create_prompt(p)
        >>> s.get_prompts_by_collection("c1")
        [p]
    """

    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Create or overwrite a prompt in storage.

        Args:
            prompt (Prompt): The prompt object to store. Must have a unique
                `id` attribute which will be used as the dictionary key.

        Returns:
            Prompt: The same prompt instance that was stored.

        Example:
            >>> storage.create_prompt(Prompt(id="p1", text="Hello"))
        """

        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its id.

        Args:
            prompt_id (str): The id of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The prompt if found, otherwise ``None``.

        Example:
            >>> storage.get_prompt("p1")
        """

        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Return a list of all stored prompts.

        Returns:
            List[Prompt]: All prompts stored in insertion-independent order.

        Example:
            >>> storage.get_all_prompts()
        """

        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt.

        Args:
            prompt_id (str): The id of the prompt to update.
            prompt (Prompt): The new prompt object that will replace the
                existing prompt stored under ``prompt_id``.

        Returns:
            Optional[Prompt]: The updated prompt if the id existed, otherwise
                ``None`` when no prompt with ``prompt_id`` is present.

        Example:
            >>> storage.update_prompt("p1", Prompt(id="p1", text="Hi"))
        """

        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by id.

        Args:
            prompt_id (str): The id of the prompt to delete.

        Returns:
            bool: ``True`` if a prompt was removed, ``False`` if no prompt
                with the given id existed.

        Example:
            >>> storage.delete_prompt("p1")
        """

        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Create or overwrite a collection in storage.

        Args:
            collection (Collection): The collection object to store. Must
                have an `id` attribute used as the key.

        Returns:
            Collection: The same collection instance that was stored.

        Example:
            >>> storage.create_collection(Collection(id="c1", name="A"))
        """

        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by id.

        Args:
            collection_id (str): The id of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection if found, otherwise ``None``.

        Example:
            >>> storage.get_collection("c1")
        """

        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Return a list of all stored collections.

        Returns:
            List[Collection]: All collections currently stored.

        Example:
            >>> storage.get_all_collections()
        """

        return list(self._collections.values())
    
    def update_collection(self, collection_id: str, collection: Collection) -> Optional[Collection]:
        if collection_id not in self._collections:
            return None
        self._collections[collection_id] = collection
        return collection
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by id.

        Args:
            collection_id (str): The id of the collection to delete.

        Returns:
            bool: ``True`` if the collection existed and was removed,
                otherwise ``False``.

        Example:
            >>> storage.delete_collection("c1")
        """

        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Return all prompts that belong to a given collection.

        Args:
            collection_id (str): The id of the collection to filter prompts by.

        Returns:
            List[Prompt]: List of prompts where ``prompt.collection_id`` matches
                ``collection_id``. Returns an empty list if none match.

        Example:
            >>> storage.get_prompts_by_collection("c1")
        """

        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Remove all prompts and collections from storage.

        This is primarily useful for tests to ensure a clean state.

        Example:
            >>> storage.clear()
        """

        self._prompts.clear()
        self._collections.clear()


# Global storage instance
#
# A convenient shared `Storage` instance for the application. Import
# `storage` from this module to access the in-memory store.
storage = Storage()

