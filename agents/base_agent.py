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
from memory import Mem0Memory

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
        self._setup_llm()

        # Initialize memory system if enabled
        if self.config.memory_enabled:
            self._setup_memory()
        else:
            self.memory = None

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

    def _setup_memory(self):
        """Set up the Mem0 memory system for the agent"""
        # Use the agent's name as its unique identifier
        self.memory = Mem0Memory(agent_id=self.config.name)

        if self.config.verbose:
            print(f"Memory system initialized for agent {self.config.name}")

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

        # If memory is enabled, retrieve relevant context from memory
        context = ""
        if self.memory and self.config.memory_enabled:
            memories = self.memory.search(task)
            if memories:
                context = "\n\nRelevant information from your memory:\n"
                for idx, memory in enumerate(memories):
                    context += f"{idx+1}. {memory['text']}\n"

        # Format the message for the LLM, including memory context if available
        messages = [
            {"role": "system", "content": self.config.system_prompt},
        ]

        # Add memory context if available
        if context:
            messages.append({"role": "system", "content": context})

        # Add the task message
        messages.append({"role": "user", "content": task})

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

        # Store in memory if memory system is enabled
        if self.memory and self.config.memory_enabled:
            interaction = [
                {"role": "user", "content": task},
                {"role": "assistant", "content": result},
            ]
            self.memory.add(
                content=interaction,
                categories=["interaction"],
                metadata={"task_type": "general"},
            )
            if self.config.verbose:
                print(f"Stored interaction in memory")

        return result

    def add_to_memory(
        self,
        content: str,
        categories: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> bool:
        """
        Add content to the agent's memory.

        Args:
            content: The content to remember
            categories: Optional categories to tag the memory with
            metadata: Additional metadata for the memory

        Returns:
            Success indicator
        """
        if not self.memory or not self.config.memory_enabled:
            if self.config.verbose:
                print(
                    f"Memory disabled for agent {self.config.name}, cannot add: {content[:50]}..."
                )
            return False

        try:
            self.memory.add(content, categories=categories, metadata=metadata)
            if self.config.verbose:
                print(f"Agent {self.config.name} remembered: {content[:50]}...")
            return True
        except Exception as e:
            if self.config.verbose:
                print(f"Error adding to memory: {str(e)}")
            return False

    def retrieve_from_memory(
        self, query: str, categories: List[str] = None, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve information from the agent's memory.

        Args:
            query: The query to search for in memory
            categories: Optional categories to filter by
            limit: Maximum number of results to return

        Returns:
            List of memory entries matching the query
        """
        if not self.memory or not self.config.memory_enabled:
            if self.config.verbose:
                print(f"Memory disabled for agent {self.config.name}, cannot retrieve")
            return []

        try:
            results = self.memory.search(
                query=query, categories=categories, limit=limit
            )

            if self.config.verbose:
                print(f"Retrieved {len(results)} memories for query: {query[:50]}...")

            return results
        except Exception as e:
            if self.config.verbose:
                print(f"Error retrieving from memory: {str(e)}")
            return []
