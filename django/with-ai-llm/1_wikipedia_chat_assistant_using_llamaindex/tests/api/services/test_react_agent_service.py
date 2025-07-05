from unittest.mock import patch, MagicMock, ANY

import pytest
from llama_index.core import VectorStoreIndex
from llama_index.core.base.response.schema import Response
from llama_index.core.tools import QueryEngineTool

from api.services.react_agent_service import ReActAgentService


@pytest.fixture
def mock_vector_index():
    return MagicMock(spec=VectorStoreIndex)


@pytest.fixture
def mock_query_engine():
    return MagicMock()


@pytest.fixture
def mock_tool():
    return MagicMock(spec=QueryEngineTool)


@pytest.fixture
def mock_llm():
    return MagicMock()


def test_initialize_agent_success(mock_tool, mock_llm):
    # Arrange
    with patch('api.services.react_agent_service.LLMConfig.get_llm', return_value=mock_llm):
        with patch('api.services.react_agent_service.ReActAgent.from_tools') as mock_from_tools:
            # Setup
            mock_agent = MagicMock()
            mock_from_tools.return_value = mock_agent
            service = ReActAgentService(max_iterations=5)

            # Act
            service.initialize_agent([mock_tool])

            # Assert
            mock_from_tools.assert_called_once_with(
                tools=[mock_tool],
                llm=mock_llm,
                max_iterations=5,
                system_prompt=ANY,  # We'll test the prompt separately
                verbose=True
            )
            assert service.agent == mock_agent
            assert service.tools == [mock_tool]


def test_query_success(mock_tool):
    # Arrange
    service = ReActAgentService()
    mock_agent = MagicMock()
    mock_response = Response(response="Test response")
    mock_agent.chat.return_value = mock_response
    service.agent = mock_agent

    # Act
    result = service.query("Test query")

    # Assert
    assert result == "Test response"
    mock_agent.chat.assert_called_once_with("Test query")


def test_query_not_initialized():
    # Arrange
    service = ReActAgentService()

    # Act & Assert
    with pytest.raises(RuntimeError, match="ReAct agent is not initialized."):
        service.query("Test query")


def test_query_empty_query(mock_tool):
    # Arrange
    service = ReActAgentService()
    mock_agent = MagicMock()
    service.agent = mock_agent

    # Act
    result = service.query("   ")

    # Assert
    assert result == "I need a question to help you. Please ask me something."
    mock_agent.chat.assert_not_called()


def test_create_wikipedia_tool_success(mock_vector_index):
    # Arrange
    mock_query_engine = MagicMock()
    mock_vector_index.as_query_engine.return_value = mock_query_engine

    # Act
    tool = ReActAgentService.create_wikipedia_tool(
        index=mock_vector_index,
        similarity_top_k=3,
        response_mode="refine"
    )

    # Assert
    assert isinstance(tool, QueryEngineTool)
    mock_vector_index.as_query_engine.assert_called_once_with(
        response_mode="refine",
        similarity_top_k=3,
        verbose=True
    )
    assert tool.metadata.name == "wikipedia_search"
    assert "Wikipedia" in tool.metadata.description


def test_create_wikipedia_tool_error(mock_vector_index):
    # Arrange
    mock_vector_index.as_query_engine.side_effect = Exception("Test error")

    # Act & Assert
    with pytest.raises(RuntimeError, match="Error creating Wikipedia query engine tool: Test error"):
        ReActAgentService.create_wikipedia_tool(mock_vector_index)


def test_system_prompt_contains_key_elements():
    # Arrange
    service = ReActAgentService()

    # Act
    prompt = service._get_system_prompt()

    # Assert
    assert "You are a helpful AI assistant with access to Wikipedia information" in prompt
    assert "wikipedia_search tool" in prompt
    assert "cite your sources" in prompt.lower()
    assert "guidelines" in prompt.lower()


def test_initialize_agent_error(mock_tool, mock_llm):
    # Arrange
    with patch('api.services.react_agent_service.LLMConfig.get_llm', return_value=mock_llm):
        with patch('api.services.react_agent_service.ReActAgent.from_tools') as mock_from_tools:
            mock_from_tools.side_effect = Exception("Initialization error")
            service = ReActAgentService()

            # Act & Assert
            with pytest.raises(RuntimeError, match="Error initializing ReAct agent: Initialization error"):
                service.initialize_agent([mock_tool])


def test_query_error(mock_tool):
    # Arrange
    service = ReActAgentService()
    mock_agent = MagicMock()
    mock_agent.chat.side_effect = Exception("Chat error")
    service.agent = mock_agent

    # Act & Assert
    with pytest.raises(RuntimeError, match="Error querying ReAct agent: Chat error"):
        service.query("Test query")