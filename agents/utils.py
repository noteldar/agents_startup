"""
Utility functions for agent operations.

This module provides helper functions and utilities for working with agents,
tasks, and related operations in the Agent Startup system.
"""

from typing import Dict, List, Any, Optional
import json


def format_task(task_description: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Format a task description with optional context for an agent.

    Args:
        task_description: The core task description
        context: Optional context data to include with the task

    Returns:
        Formatted task string
    """
    if not context:
        return task_description

    context_str = "\n\n**Context:**\n"
    for key, value in context.items():
        if isinstance(value, (dict, list)):
            context_str += f"\n{key}:\n{json.dumps(value, indent=2)}\n"
        else:
            context_str += f"\n{key}: {value}\n"

    return f"{task_description}\n{context_str}"


def parse_agent_response(response: str) -> Dict[str, Any]:
    """
    Parse a structured response from an agent.

    Attempts to extract structured data from an agent's response,
    looking for JSON-like sections or specific markers.

    Args:
        response: The raw response from the agent

    Returns:
        Dictionary containing parsed data, with at least a 'raw_response' field
    """
    result = {"raw_response": response}

    # Look for JSON patterns
    try:
        # Try to find JSON-like content between triple backticks
        if "```json" in response and "```" in response.split("```json")[1]:
            json_str = response.split("```json")[1].split("```")[0].strip()
            parsed = json.loads(json_str)
            result["parsed_data"] = parsed
        # If no explicit JSON blocks, look for dictionary-like patterns
        elif "{" in response and "}" in response:
            potential_json = response[response.find("{") : response.rfind("}") + 1]
            parsed = json.loads(potential_json)
            result["parsed_data"] = parsed
    except (json.JSONDecodeError, IndexError):
        # If parsing fails, include the 'parsed' key but set it to None
        result["parsed_data"] = None

    return result


def extract_key_information(response: str, keywords: List[str]) -> Dict[str, List[str]]:
    """
    Extract sentences containing key information based on keywords.

    Args:
        response: The text to analyze
        keywords: List of keywords to look for

    Returns:
        Dictionary mapping keywords to relevant sentences
    """
    results = {keyword: [] for keyword in keywords}

    # Split text into sentences (simple approach)
    sentences = [s.strip() for s in response.replace("\n", " ").split(".") if s.strip()]

    # Check each sentence for keywords
    for sentence in sentences:
        for keyword in keywords:
            if keyword.lower() in sentence.lower():
                results[keyword].append(sentence)

    return results
