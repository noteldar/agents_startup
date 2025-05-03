# Agent Startup Project Documentation

## Overview
Agent Startup is a multi-agent system designed to solve complex internet research tasks by leveraging four persistent AI agents working collaboratively. Each agent has a unique role, persistent memory, and access to web search tools.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd agents_startup
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
LLAMA_API_KEY=your_llama_api_key
MEM0_API_KEY=your_mem0_api_key 
SEARCH_API_KEY=your_search_api_key
```

## Project Structure
- `agents/`: Contains agent classes and behavior definitions
- `memory/`: Memory system (mem0) integration
- `tools/`: Web search and other tool implementations
- `protocols/`: Chat and meeting protocols
- `main.py`: Entry point for running the system

## Getting Started
After installation and setup, you can run the system with:
```bash
python main.py
```

## Agents and Roles
- CEO Agent: Coordinates the team, decomposes problems, and assigns tasks
- Researcher Agent: Specializes in gathering information from the web
- Analyst Agent: Focuses on critical thinking and analysis of information
- Synthesizer Agent: Compiles and presents knowledge in a clear format

## Memory System
The system uses [Mem0](https://mem0.ai) for persistent memory storage and retrieval:

### Memory Types
- **Agent Memory**: Each agent has its own long-term memory stored with `agent_id`
- **User Memory**: Information about users stored with `user_id`
- **Session Memory**: Short-term memory for a specific interaction session using `run_id`

### Memory Features
- **Semantic Search**: Retrieve relevant memories based on meaning, not just keywords
- **Categorized Storage**: Tag memories with categories for better organization
- **Metadata Support**: Attach structured metadata to memories for advanced filtering
- **Memory History**: Track changes to memories over time

### Testing the Memory System
You can test the memory system functionality with:
```bash
python -m memory.test_memory
```

## References
- PydanticAI documentation: https://ai.pydantic.dev/
- mem0 repository: https://github.com/mem0ai/mem0
- Llama API: https://github.com/meta-llama/llama-api-python 
- Mem0 Documentation: https://docs.mem0.ai/platform/quickstart 