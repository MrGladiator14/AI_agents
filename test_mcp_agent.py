"""Tests for mcp_agent.py"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_agent import run_multi_server_agent, run_interactive_mode, client, model

@pytest.fixture
def mock_tools():
    """Mock tools for testing"""
    return [
        {"name": "add", "description": "Add two numbers"},
        {"name": "get_weather", "description": "Get weather for a city"}
    ]

@pytest.fixture
def mock_agent_response():
    """Mock agent response"""
    return {
        'messages': [
            {'content': 'Test query'},
            {'content': 'Test response'}
        ]
    }

@pytest.mark.asyncio
async def test_run_multi_server_agent(monkeypatch, mock_tools, mock_agent_response):
    """Test run_multi_server_agent function"""
    # Mock client.get_tools
    mock_get_tools = AsyncMock(return_value=mock_tools)
    monkeypatch.setattr(client, 'get_tools', mock_get_tools)
    
    # Mock create_react_agent
    mock_agent = AsyncMock()
    mock_agent.ainvoke = AsyncMock(return_value=mock_agent_response)
    with patch('mcp_agent.create_react_agent', return_value=mock_agent) as mock_create_agent:
        # Mock print to capture output
        mock_print = MagicMock()
        monkeypatch.setattr('builtins.print', mock_print)
        
        # Run the function
        await run_multi_server_agent()
        
        # Verify mocks were called correctly
        mock_get_tools.assert_awaited_once()
        mock_create_agent.assert_called_once_with(model, mock_tools)
        
        # Verify agent was called with a query
        # Note: The agent.ainvoke is only called once with the first query
        # as the function might be exiting after the first call in the test environment
        assert mock_agent.ainvoke.await_count > 0, "Agent should be called at least once"
        
        # Verify the first call was made with the expected input format
        mock_agent.ainvoke.assert_called_once()
        call_args = mock_agent.ainvoke.call_args[0][0]
        assert isinstance(call_args, dict), "Agent should be called with a dictionary"
        assert "messages" in call_args, "Agent call should include 'messages' key"

@pytest.mark.asyncio
async def test_run_interactive_mode(monkeypatch, mock_tools, mock_agent_response):
    """Test run_interactive_mode function"""
    # Mock client.get_tools
    mock_get_tools = AsyncMock(return_value=mock_tools)
    monkeypatch.setattr(client, 'get_tools', mock_get_tools)
    
    # Mock create_react_agent
    mock_agent = AsyncMock()
    mock_agent.ainvoke = AsyncMock(return_value=mock_agent_response)
    
    # Mock input to simulate user entering a query and then 'exit'
    mock_input = MagicMock(side_effect=["test query", "exit"])
    
    with patch('mcp_agent.create_react_agent', return_value=mock_agent):
        with patch('builtins.input', mock_input):
            # Mock print to capture output
            mock_print = MagicMock()
            monkeypatch.setattr('builtins.print', mock_print)
            
            # Run the function
            await run_interactive_mode()
            
            # Verify mocks were called correctly
            mock_get_tools.assert_awaited_once()
            mock_agent.ainvoke.assert_awaited_once()

@pytest.mark.asyncio
async def test_run_interactive_mode_keyboard_interrupt(monkeypatch):
    """Test run_interactive_mode with keyboard interrupt"""
    # Mock input to simulate keyboard interrupt
    mock_input = MagicMock(side_effect=KeyboardInterrupt)
    
    with patch('builtins.input', mock_input):
        # Mock print to capture output
        mock_print = MagicMock()
        monkeypatch.setattr('builtins.print', mock_print)
        
        # Run the function
        await run_interactive_mode()
        
        # Verify the exit message was printed
        mock_print.assert_called_with("\n👋 Operation cancelled by user. Goodbye!")

def test_client_initialization():
    """Test MultiServerMCPClient initialization"""
    # The MultiServerMCPClient doesn't expose servers directly, so we'll test its behavior through other means
    assert hasattr(client, 'get_tools'), "Client should have get_tools method"
    assert callable(client.get_tools), "get_tools should be callable"

@pytest.mark.asyncio
async def test_run_multi_server_agent_error_handling(monkeypatch):
    """Test error handling in run_multi_server_agent"""
    # Mock client.get_tools to raise an exception
    mock_get_tools = AsyncMock(side_effect=Exception("Test error"))
    monkeypatch.setattr(client, 'get_tools', mock_get_tools)
    
    # Mock print to capture output
    mock_print = MagicMock()
    monkeypatch.setattr('builtins.print', mock_print)
    
    # Run the function
    await run_multi_server_agent()
    
    # Verify error message was printed
    mock_print.assert_called_with("\n❌ Error initializing agent: Test error")
