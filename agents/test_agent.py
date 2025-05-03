"""
Test script for the base agent implementation.

This script creates a simple agent and runs it on a test task
to verify the basic functionality is working correctly.
"""

import os
from dotenv import load_dotenv
from agents.base_agent import BaseAgent, AgentConfig

# Ensure environment variables are loaded
load_dotenv()


def test_base_agent():
    """Test the basic functionality of the BaseAgent class"""

    # Create a test agent configuration
    agent_config = AgentConfig(
        name="Research Assistant",
        role="AI Research Specialist",
        goal="Find and provide accurate information on requested topics",
        backstory="You are an advanced AI research assistant built to help users find and analyze information. You have access to various sources of information and can process complex queries.",
        verbose=True,
    )

    # Create the agent
    agent = BaseAgent(config=agent_config)

    # Test a simple task
    test_task = (
        "What are the key benefits of using multi-agent systems for complex tasks?"
    )

    print(f"\nTesting agent with task: {test_task}\n")
    print("-" * 50)

    try:
        response = agent.run(test_task)
        print(f"Agent response:\n{response}\n")
        print("-" * 50)
        print("Test completed successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    # Check if Llama API key is set
    if not os.getenv("LLAMA_API_KEY"):
        print("Error: LLAMA_API_KEY environment variable is not set.")
        print("Please set this variable in your .env file or environment.")
        exit(1)

    # Run the test
    test_base_agent()
