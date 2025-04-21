import pytest
from src.agents.base_agent import BaseAgent

@pytest.fixture
def base_agent():
    """Fixture to create a BaseAgent instance"""
    return BaseAgent()

@pytest.mark.asyncio
async def test_base_agent_initialization(base_agent):
    """Test that BaseAgent initializes with default values"""
    assert isinstance(base_agent, BaseAgent)
    assert base_agent.model == "gpt-4o"

@pytest.mark.asyncio
async def test_base_agent_execute_basic(base_agent):
    """Test basic execution of BaseAgent with a simple prompt"""
    system_prompt = "You are a helpful assistant."
    user_input = "Say 'Hello, World!'"
    
    response = await base_agent.execute(
        system_prompt=system_prompt,
        user_input=user_input
    )
    
    assert isinstance(response, str)
    assert len(response) > 0
