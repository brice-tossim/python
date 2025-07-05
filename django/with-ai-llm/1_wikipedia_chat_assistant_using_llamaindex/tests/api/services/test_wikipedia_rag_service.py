import pytest
from unittest.mock import patch, MagicMock, ANY
from llama_index.core.schema import Document
from llama_index.core import VectorStoreIndex

from api.services.wikipedia_rag_service import WikipediaRagService


@pytest.fixture
def mock_services():
    with patch('api.services.wikipedia_rag_service.WikipediaTitleExtractorService') as mock_extractor, \
            patch('api.services.wikipedia_rag_service.WikipediaContentService') as mock_fetcher, \
            patch('api.services.wikipedia_rag_service.VectorIndexingService') as mock_indexer, \
            patch('api.services.wikipedia_rag_service.ReActAgentService') as mock_agent_svc:
        # Setup mock services
        mock_extractor.return_value.extract_titles.return_value = ["Python", "Django"]

        mock_doc = Document(text="Test content")
        mock_fetcher.return_value.fetch_content.return_value = [mock_doc]

        mock_index = MagicMock(spec=VectorStoreIndex)
        mock_indexer.return_value.create_index_from_documents.return_value = mock_index

        mock_tool = MagicMock()
        mock_agent_svc.return_value.create_wikipedia_tool.return_value = mock_tool

        yield {
            'extractor': mock_extractor,
            'fetcher': mock_fetcher,
            'indexer': mock_indexer,
            'agent_svc': mock_agent_svc
        }


def test_create_agent_success(mock_services):
    # Arrange
    service = WikipediaRagService()

    # Act
    service.create_agent("Test query")

    # Assert
    mock_services['extractor'].return_value.extract_titles.assert_called_once_with("Test query")
    mock_services['fetcher'].return_value.fetch_content.assert_called_once_with(["Python", "Django"])
    mock_services['indexer'].return_value.create_index_from_documents.assert_called_once()
    mock_services['agent_svc'].return_value.create_wikipedia_tool.assert_called_once()
    mock_services['agent_svc'].return_value.initialize_agent.assert_called_once()
    assert service._is_agent_initialized is True


def test_create_agent_no_titles(mock_services):
    # Arrange
    mock_services['extractor'].return_value.extract_titles.return_value = []
    service = WikipediaRagService()

    # Act & Assert
    with pytest.raises(RuntimeError, match="No relevant Wikipedia pages found"):
        service.create_agent("Test query")
    assert service._is_agent_initialized is False


def test_create_agent_no_documents(mock_services):
    # Arrange
    mock_services['fetcher'].return_value.fetch_content.return_value = []
    service = WikipediaRagService()

    # Act & Assert
    with pytest.raises(RuntimeError, match="Failed to fetch content from Wikipedia"):
        service.create_agent("Test query")


def test_create_agent_no_index(mock_services):
    # Arrange
    mock_services['indexer'].return_value.create_index_from_documents.return_value = None
    service = WikipediaRagService()

    # Act & Assert
    with pytest.raises(RuntimeError, match="Failed to create vector index"):
        service.create_agent("Test query")


def test_query_first_time(mock_services):
    # Arrange
    mock_services['agent_svc'].return_value.query.return_value = "Test response"
    service = WikipediaRagService()

    # Act
    result = service.query("Test query")

    # Assert
    assert result == "Test response"
    mock_services['agent_svc'].return_value.query.assert_called_once_with("Test query")


def test_query_subsequent_calls(mock_services):
    # Arrange
    mock_services['agent_svc'].return_value.query.return_value = "Test response"
    service = WikipediaRagService()
    service._is_agent_initialized = True

    # Act
    result = service.query("Another query")

    # Assert
    assert result == "Test response"
    mock_services['extractor'].return_value.extract_titles.assert_not_called()


def test_query_handles_runtime_error(mock_services):
    # Arrange
    mock_services['extractor'].return_value.extract_titles.return_value = []
    service = WikipediaRagService()

    # Act
    result = service.query("Invalid query")

    # Assert
    assert "I'm sorry, I couldn't process your query" in result


def test_query_handles_unexpected_error(mock_services):
    # Arrange
    mock_services['agent_svc'].return_value.query.side_effect = Exception("Unexpected error")
    service = WikipediaRagService()
    service._is_agent_initialized = True

    # Act
    result = service.query("Test query")

    # Assert
    assert "unexpected error" in result.lower()


def test_initialization():
    # Arrange & Act
    service = WikipediaRagService()

    # Assert
    assert service._is_agent_initialized is False
    assert hasattr(service, 'title_extractor')
    assert hasattr(service, 'content_fetcher')
    assert hasattr(service, 'vector_indexer')
    assert hasattr(service, 'agent_service')