#!/usr/bin/env python3
"""
Agent Startup - Multi-agent system for collaborative problem solving
"""

import os
import argparse
from dotenv import load_dotenv
from agents import BaseAgent, AgentConfig

# Load environment variables
load_dotenv()


def run_single_agent(task):
    """Run a single agent on the specified task for testing"""
    # Check if Llama API key is set
    if not os.getenv("LLAMA_API_KEY"):
        print("Error: LLAMA_API_KEY environment variable is not set.")
        print("Please set this variable in your .env file or environment.")
        return

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

    print(f"\nRunning agent with task: {task}\n")
    print("-" * 50)

    try:
        response = agent.run(task)
        print(f"Agent response:\n{response}\n")
        print("-" * 50)
    except Exception as e:
        print(f"Error occurred: {e}")


def main():
    """Main entry point for the Agent Startup system"""
    parser = argparse.ArgumentParser(description="Agent Startup - Multi-agent system")
    parser.add_argument(
        "--task", type=str, help="Research task for the agents to solve"
    )
    args = parser.parse_args()

    print("Agent Startup initializing...")

    if args.task:
        print(f"Starting research on task: {args.task}")
        run_single_agent(args.task)
    else:
        print("No task specified. Use --task to provide a research question.")

    print(
        "System initialized. Agent framework will be implemented in subsequent steps."
    )


if __name__ == "__main__":
    main()
