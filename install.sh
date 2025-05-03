#!/bin/bash
# Installation script for Agent Startup

# Define colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Setting up Agent Startup environment ===${NC}"

# Check if Python 3.9+ is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}')
if [[ -z "$python_version" ]]; then
    echo -e "${RED}Python 3 not found. Please install Python 3.9 or later.${NC}"
    exit 1
fi

echo -e "${GREEN}Using Python version: $python_version${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment. Please install venv package.${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate virtual environment.${NC}"
    exit 1
fi

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install dependencies.${NC}"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from example...${NC}"
    cp env.example .env
    echo -e "${YELLOW}Please edit the .env file to set your Llama API key.${NC}"
fi

echo -e "${GREEN}=== Setup complete! ===${NC}"
echo -e "To activate the environment: ${YELLOW}source venv/bin/activate${NC}"
echo -e "To run the agent: ${YELLOW}python main.py --task \"your research question\"${NC}"
echo -e "To run tests: ${YELLOW}python agents/test_agent.py${NC}" 