"""
Base Agent implementation for the Agent Startup system.

This class serves as the foundation for all agent types in the system,
providing common functionality and integration with Llama models.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from llama_api_client import LlamaAPIClient
import os
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()


class AgentConfig(BaseModel):
    """Configuration for an agent instance"""

    name: str = Field(..., description="The name of the agent")
    role: str = Field(..., description="The role this agent serves in the team")
    goal: str = Field(..., description="The agent's primary goal or purpose")
    backstory: str = Field(
        ..., description="Background story for the agent to provide context"
    )
    verbose: bool = Field(
        default=False, description="Whether the agent should provide verbose output"
    )
    memory_enabled: bool = Field(
        default=True, description="Whether the agent's memory system is enabled"
    )
    allow_delegation: bool = Field(
        default=True, description="Whether the agent can delegate tasks to other agents"
    )
    llm_model: str = Field(
        default="Llama-4-Maverick-17B-128E-Instruct-FP8",
        description="LLM model identifier to use",
    )
    temperature: float = Field(
        default=0.7, description="Temperature setting for the LLM"
    )
    max_tokens: int = Field(
        default=2000, description="Maximum number of tokens in responses"
    )
    system_prompt: Optional[str] = Field(
        default=None, description="Custom system prompt to use"
    )


class BaseAgent:
    """
    Base Agent class using CrewAI concepts and Llama integration.

    This implements the core agent functionality used across all agent types
    in the system, providing a unified interface for agent interactions.
    """

    def __init__(self, config: AgentConfig):
        """
        Initialize a new agent with the given configuration.

        Args:
            config: An AgentConfig object containing the agent's configuration
        """
        self.config = config
        self.memory = None  # Will be initialized later with mem0
        self._setup_llm()

        # Build the system prompt if not provided
        if not self.config.system_prompt:
            self.config.system_prompt = self._build_default_system_prompt()

        # Track agent state
        self.current_task = None
        self.message_history = []

    def _setup_llm(self):
        """Set up the Llama language model client"""
        api_key = os.getenv("LLAMA_API_KEY")
        if not api_key:
            raise ValueError("LLAMA_API_KEY environment variable is required")

        self.llm = LlamaAPIClient(api_key=api_key)

    def _build_default_system_prompt(self) -> str:
        """
        Build a default system prompt based on the agent's configuration.
        This can be overridden by specific agent types.
        """
        return f"""
        You are {self.config.name}, a {self.config.role}.
        
        Your backstory: {self.config.backstory}
        
        Your goal is to: {self.config.goal}
        
        When working on tasks, you should:
        - Think carefully about what information you need
        - Break down complex problems into smaller steps
        - Use your expertise to generate high-quality responses
        - Be helpful, accurate, and focused on your goal
        
        Please respond in a professional and helpful manner.
        """

    def run(self, task: str) -> str:
        """
        Run the agent on a specific task.

        Args:
            task: The task description to work on

        Returns:
            The agent's response to the task
        """
        self.current_task = task

        # Format the message for the LLM
        messages = [
            {"role": "system", "content": self.config.system_prompt},
            {"role": "user", "content": task},
        ]

        # Call the Llama model with correct parameters according to SDK
        response = self.llm.chat.completions.create(
            model=self.config.llm_model,
            messages=messages,
            temperature=self.config.temperature,
            max_completion_tokens=self.config.max_tokens,  # Changed from max_tokens
        )

        # Extract and return the response content
        result = response.completion_message.content.text

        # Record this interaction in history
        self.message_history.append({"task": task, "response": result})

        # TODO: Store in memory once memory system is implemented

        return result

    def add_to_memory(self, content: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Add content to the agent's memory.
        Will be fully implemented when the memory system is integrated.

        Args:
            content: The content to remember
            metadata: Additional metadata for the memory

        Returns:
            Success indicator
        """
        # Placeholder until memory system is implemented
        print(f"Agent {self.config.name} would remember: {content[:50]}...")
        return True

    def retrieve_from_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve information from the agent's memory.
        Will be fully implemented when the memory system is integrated.

        Args:
            query: The query to search for in memory
            limit: Maximum number of results to return

        Returns:
            List of memory entries matching the query
        """
        # Placeholder until memory system is implemented
        return []
