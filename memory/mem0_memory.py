"""
Mem0 Memory implementation for Agent Startup system.

This module provides memory capabilities for agents using the Mem0 platform.
"""

import os
from typing import Dict, List, Any, Optional, Union
from dotenv import load_dotenv
from mem0 import MemoryClient

# Ensure environment variables are loaded
load_dotenv()


class Mem0Memory:
    """Memory implementation using Mem0 platform for agent memory."""

    def __init__(self, agent_id: str = None, user_id: str = None):
        """
        Initialize the Mem0 memory system.

        Args:
            agent_id: Unique identifier for the agent (used for agent-specific memories)
            user_id: Unique identifier for the user (used for user-specific memories)
        """
        self.agent_id = agent_id
        self.user_id = user_id
        self._setup_client()

    def _setup_client(self):
        """Set up the Mem0 client with API key from environment variables."""
        api_key = os.getenv("MEM0_API_KEY")
        if not api_key:
            raise ValueError("MEM0_API_KEY environment variable is required")

        # Set API key in environment (as recommended in Mem0 docs)
        os.environ["MEM0_API_KEY"] = api_key

        # Create the Mem0 client
        self.client = MemoryClient()

    def add(
        self,
        content: Union[str, List[Dict[str, str]]],
        categories: List[str] = None,
        metadata: Dict[str, Any] = None,
        run_id: str = None,
    ) -> Dict[str, Any]:
        """
        Add content to memory.

        Args:
            content: Either a string or a list of message objects in the format
                    [{"role": "user", "content": "message"}, ...]
            categories: Optional categories to tag the memory with
            metadata: Optional metadata to associate with the memory
            run_id: Optional session/run identifier for short-term memory

        Returns:
            Response from Mem0 API
        """
        # Determine the memory identifiers to use
        mem_args = {"output_format": "v1.1"}
        if self.user_id:
            mem_args["user_id"] = self.user_id
        if self.agent_id:
            mem_args["agent_id"] = self.agent_id
        if run_id:
            mem_args["run_id"] = run_id
        if categories:
            mem_args["categories"] = categories

        # Add metadata if provided
        if metadata:
            mem_args["metadata"] = metadata

        # If content is a string, convert to message format
        if isinstance(content, str):
            messages = [
                {"role": "user" if self.user_id else "assistant", "content": content}
            ]
        else:
            messages = content

        # Add to memory using Mem0 client
        return self.client.add(messages, **mem_args)

    def search(
        self,
        query: str,
        threshold: float = 0.1,
        categories: List[str] = None,
        metadata: Dict[str, Any] = None,
        limit: int = 5,
        run_id: str = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant memories based on a query.

        Args:
            query: The search query
            threshold: Relevance threshold (0-1)
            categories: Optional categories to filter by
            metadata: Optional metadata to filter by
            limit: Maximum number of results to return
            run_id: Optional session/run identifier to filter by

        Returns:
            List of relevant memories
        """
        # Determine the memory identifiers to use
        search_args = {"limit": limit, "threshold": threshold, "output_format": "v1.1"}
        if self.user_id:
            search_args["user_id"] = self.user_id
        if self.agent_id:
            search_args["agent_id"] = self.agent_id
        if run_id:
            search_args["run_id"] = run_id
        if categories:
            search_args["categories"] = categories
        if metadata:
            search_args["metadata"] = metadata

        # Search in memory using Mem0 client
        response = self.client.search(query, **search_args)

        # Process response based on format
        # Mem0 API returns different formats
        if isinstance(response, dict):
            if "memories" in response:
                return response["memories"]
            elif "results" in response:
                return response["results"]

        return response

    def get_all(
        self,
        categories: List[str] = None,
        metadata: Dict[str, Any] = None,
        keywords: str = None,
        run_id: str = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        """
        Get all memories for the current agent/user.

        Args:
            categories: Optional categories to filter by
            metadata: Optional metadata to filter by
            keywords: Optional keywords to filter by
            run_id: Optional session/run identifier to filter by
            page: Page number for pagination
            page_size: Number of results per page

        Returns:
            Dict containing memories and pagination info
        """
        # Determine the memory identifiers to use
        get_args = {"page": page, "page_size": page_size}
        if self.user_id:
            get_args["user_id"] = self.user_id
        if self.agent_id:
            get_args["agent_id"] = self.agent_id
        if run_id:
            get_args["run_id"] = run_id
        if categories:
            get_args["categories"] = categories
        if keywords:
            get_args["keywords"] = keywords

        # Get memories using Mem0 client
        return self.client.get_all(**get_args)

    def get(self, memory_id: str) -> Dict[str, Any]:
        """
        Get a specific memory by ID.

        Args:
            memory_id: The ID of the memory to retrieve

        Returns:
            The memory object
        """
        return self.client.get(memory_id)

    def update(self, memory_id: str, content: str) -> Dict[str, Any]:
        """
        Update a specific memory.

        Args:
            memory_id: The ID of the memory to update
            content: The new content for the memory

        Returns:
            The updated memory object
        """
        return self.client.update(memory_id, content)

    def delete(self, memory_id: str = None) -> Dict[str, Any]:
        """
        Delete a specific memory or all memories for the current agent/user.

        Args:
            memory_id: The ID of the memory to delete (if None, deletes all)

        Returns:
            Response from Mem0 API
        """
        if memory_id:
            return self.client.delete(memory_id)

        # Delete all memories for this agent/user
        if self.user_id:
            return self.client.delete_all(user_id=self.user_id)
        elif self.agent_id:
            return self.client.delete_all(agent_id=self.agent_id)

        # Safety check - don't delete everything unless explicitly intended
        raise ValueError(
            "Either memory_id, user_id, or agent_id must be specified for deletion"
        )

    def get_history(self, memory_id: str) -> List[Dict[str, Any]]:
        """
        Get the history of changes for a specific memory.

        Args:
            memory_id: The ID of the memory to get history for

        Returns:
            List of historical versions of the memory
        """
        return self.client.history(memory_id)
