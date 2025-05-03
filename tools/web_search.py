"""
Web search tool implementation for the Agent Startup system.
This tool allows agents to search the web for information.
"""

import os
import json
import logging
import requests
from typing import List, Dict, Any, Optional
from pydantic_ai.tools import Tool
from pydantic import Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSearchResult:
    """Represents a single search result from a web search."""

    def __init__(self, title: str, url: str, snippet: str):
        self.title = title
        self.url = url
        self.snippet = snippet

    def __str__(self) -> str:
        return f"Title: {self.title}\nURL: {self.url}\nSnippet: {self.snippet}\n"

    def to_dict(self) -> Dict[str, str]:
        return {"title": self.title, "url": self.url, "snippet": self.snippet}


async def execute_web_search(query: str, num_results: int = 5) -> List[WebSearchResult]:
    """
    Execute a web search using a search API.

    Args:
        query: The search query
        num_results: Number of results to return (default: 5)

    Returns:
        A list of WebSearchResult objects containing the search results
    """
    # Get the API key from environment variables
    api_key = os.environ.get("SEARCH_API_KEY")
    if not api_key:
        logger.error("SEARCH_API_KEY environment variable is not set")
        return [
            WebSearchResult(
                title="Error: API key not found",
                url="",
                snippet="The search API key was not found. Please set the SEARCH_API_KEY environment variable.",
            )
        ]

    # In a real implementation, this would use an actual search API
    # For now, we'll implement a simple mock response
    try:
        # This is a placeholder for a real API call
        # In a real implementation, you'd make a call similar to:
        # response = requests.get(
        #     "https://api.search-provider.com/search",
        #     params={
        #         "q": query,
        #         "count": num_results,
        #         "api_key": api_key
        #     }
        # )
        # response.raise_for_status()
        # results = response.json()

        # For development, return mock results
        mock_results = [
            WebSearchResult(
                title=f"Search result {i+1} for '{query}'",
                url=f"https://example.com/result{i+1}",
                snippet=f"This is a mock search result {i+1} for the query '{query}'. In a real implementation, this would contain an actual snippet from a web page.",
            )
            for i in range(num_results)
        ]

        logger.info(f"Web search for '{query}' returned {len(mock_results)} results")
        return mock_results

    except Exception as e:
        logger.error(f"Error executing web search: {str(e)}")
        return [
            WebSearchResult(
                title="Error: Search failed",
                url="",
                snippet=f"The search operation failed with error: {str(e)}",
            )
        ]


def web_search_tool() -> Tool:
    """
    Create a web search tool that can be used by agents.

    Returns:
        A Tool instance that can be added to an agent
    """

    async def search_web_api(query: str, num_results: int = 5) -> str:
        """
        Search the web for information based on the query.

        Args:
            query: The search query
            num_results: Number of results to return (default: 5)

        Returns:
            A formatted string containing the search results
        """
        results = await execute_web_search(query, num_results)

        # Format the results as a string
        formatted_results = "\n\n".join([str(result) for result in results])
        return f"Search results for '{query}':\n\n{formatted_results}"

    # Create and return the tool
    return Tool(
        name="web_search",
        description="Search the web for information based on the query.",
        function=search_web_api,
        schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find information on the web",
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return (default: 5)",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    )
