"""
Test script to demonstrate and validate the Mem0Memory implementation.
"""

import os
from dotenv import load_dotenv
from memory import Mem0Memory

# Ensure environment variables are loaded
load_dotenv()


def test_memory_basic():
    """Test basic memory operations."""
    print("\n----- Basic Memory Test -----")

    # Initialize memory for a test agent
    memory = Mem0Memory(agent_id="test-agent")

    # Add a simple memory
    print("Adding a simple memory...")
    result = memory.add("This is a test memory from the agent.")
    print(f"Add result: {result}")

    # Search for that memory
    print("\nSearching for the memory...")
    memories = memory.search("test memory")
    print(f"Found {len(memories)} memories")
    for mem in memories:
        memory_text = mem.get("memory", mem.get("text", "No text"))
        memory_id = mem.get("id", "No ID")
        print(f"- {memory_text} (ID: {memory_id})")

    # If we found any memories, test updating one
    if memories:
        memory_id = memories[0].get("id")
        print(f"\nUpdating memory {memory_id}...")
        update_result = memory.update(memory_id, "This is an UPDATED test memory!")
        print(f"Update result: {update_result}")

        # Get memory history
        print(f"\nGetting memory history for {memory_id}...")
        history = memory.get_history(memory_id)
        print(f"History contains {len(history)} versions")
        for idx, version in enumerate(history):
            version_text = version.get("memory", version.get("text", "No text"))
            print(f"  Version {idx+1}: {version_text}")

        # Delete the memory
        print(f"\nDeleting memory {memory_id}...")
        delete_result = memory.delete(memory_id)
        print(f"Delete result: {delete_result}")


def test_memory_conversation():
    """Test memory with a simulated conversation."""
    print("\n----- Conversation Memory Test -----")

    # Initialize memory for a test user and agent
    user_memory = Mem0Memory(user_id="test-user")
    agent_memory = Mem0Memory(agent_id="test-agent")

    # Simulate a conversation
    conversation = [
        {"role": "user", "content": "My name is Alice and I live in New York."},
        {
            "role": "assistant",
            "content": "Nice to meet you, Alice! How do you like living in New York?",
        },
        {"role": "user", "content": "I love it, especially Central Park."},
        {
            "role": "assistant",
            "content": "Central Park is wonderful. What do you enjoy doing there?",
        },
    ]

    # Add conversation to both user and agent memories
    print("Adding conversation to memories...")
    user_result = user_memory.add(
        conversation, categories=["personal_info", "location"]
    )
    agent_result = agent_memory.add(
        conversation, categories=["user_preferences"], metadata={"location": "New York"}
    )

    print(f"User memory add result: {user_result}")
    print(f"Agent memory add result: {agent_result}")

    # Search for something the user said
    print("\nSearching user memories for 'New York'...")
    user_memories = user_memory.search("New York")
    print(f"Found {len(user_memories)} user memories about New York")
    for mem in user_memories:
        memory_text = mem.get("memory", mem.get("text", "No text"))
        print(f"- {memory_text}")

    # Search for something about the conversation from agent's perspective
    print("\nSearching agent memories for 'Central Park'...")
    agent_memories = agent_memory.search("Central Park")
    print(f"Found {len(agent_memories)} agent memories about Central Park")
    for mem in agent_memories:
        memory_text = mem.get("memory", mem.get("text", "No text"))
        print(f"- {memory_text}")

    # Get all memories with specific category
    print("\nGetting all user memories with category 'location'...")
    all_location_memories = user_memory.get_all(categories=["location"])
    print(f"Found {len(all_location_memories.get('memories', []))} location memories")

    # Clean up test data
    print("\nCleaning up test memories...")
    user_cleanup = user_memory.delete()
    agent_cleanup = agent_memory.delete()
    print(f"User memory cleanup result: {user_cleanup}")
    print(f"Agent memory cleanup result: {agent_cleanup}")


if __name__ == "__main__":
    if not os.getenv("MEM0_API_KEY"):
        print("ERROR: MEM0_API_KEY environment variable not set!")
        print("Please set this variable in your .env file or environment.")
        exit(1)

    print("=== Mem0 Memory System Test ===")
    test_memory_basic()
    test_memory_conversation()
    print("\n=== All tests completed ===")
