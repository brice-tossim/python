from unittest.mock import patch, MagicMock

from llama_index.core import Document
from llama_index.core.schema import TextNode

from api.services.vector_indexing_service import VectorIndexingService


def test_create_index_from_documents_success():
    # Arrange
    mock_doc1 = Document(text="This is a test document.")
    mock_doc2 = Document(text="Another test document.")
    documents = [mock_doc1, mock_doc2]

    mock_nodes = [
        TextNode(text="This is a test document."),
        TextNode(text="Another test document.")
    ]

    with patch('api.services.vector_indexing_service.SentenceSplitter') as mock_splitter_cls:
        # Setup mock splitter
        mock_splitter = MagicMock()
        mock_splitter.get_nodes_from_documents.return_value = mock_nodes
        mock_splitter_cls.return_value = mock_splitter

        # Get a reference to the actual VectorStoreIndex class
        with patch('api.services.vector_indexing_service.VectorStoreIndex') as mock_index_cls:
            # Create a mock for the index instance
            mock_index_instance = MagicMock()
            mock_index_cls.return_value = mock_index_instance

            service = VectorIndexingService(chunk_size=150, chunk_overlap=40)

            # Act
            result = service.create_index_from_documents(documents)

            # Assert
            assert result == mock_index_instance
            mock_splitter_cls.assert_called_once_with(
                chunk_size=150,
                chunk_overlap=40
            )
            mock_splitter.get_nodes_from_documents.assert_called_once_with(documents)

            # Check that VectorStoreIndex was called with the nodes
            mock_index_cls.assert_called_once()
            args, kwargs = mock_index_cls.call_args
            if args:  # If nodes were passed as positional argument
                assert args[0] == mock_nodes
            else:  # If nodes were passed as keyword argument
                assert kwargs.get('nodes') == mock_nodes


def test_create_index_from_documents_empty_input():
    # Arrange
    service = VectorIndexingService()

    # Act
    result = service.create_index_from_documents([])

    # Assert
    assert result is None


def test_create_index_from_documents_with_chunking():
    # Arrange
    long_text = " ".join(["sentence"] * 200)  # Create a long text that will be chunked
    document = Document(text=long_text)

    with patch('api.services.vector_indexing_service.SentenceSplitter') as mock_splitter_cls:
        mock_splitter = MagicMock()
        mock_nodes = [TextNode(text="chunk 1"), TextNode(text="chunk 2")]
        mock_splitter.get_nodes_from_documents.return_value = mock_nodes
        mock_splitter_cls.return_value = mock_splitter

        with patch('api.services.vector_indexing_service.VectorStoreIndex'):
            service = VectorIndexingService(chunk_size=100, chunk_overlap=20)

            # Act
            result = service.create_index_from_documents([document])

            # Assert
            assert result is not None
            mock_splitter.get_nodes_from_documents.assert_called_once()
            args, _ = mock_splitter.get_nodes_from_documents.call_args
            assert len(args[0]) == 1
            assert args[0][0].text == long_text


def test_create_index_from_documents_handles_exception():
    # Arrange
    mock_doc = Document(text="Test document")

    with patch('api.services.vector_indexing_service.SentenceSplitter') as mock_splitter_cls:
        mock_splitter = MagicMock()
        mock_splitter.get_nodes_from_documents.side_effect = Exception("Split error")
        mock_splitter_cls.return_value = mock_splitter

        service = VectorIndexingService()

        # Act
        result = service.create_index_from_documents([mock_doc])

        # Assert
        assert result is None


def test_default_initialization():
    # Arrange & Act
    service = VectorIndexingService()

    # Assert
    assert service.chunk_size == 150
    assert service.chunk_overlap == 40
    assert service.splitter is not None


def test_custom_initialization():
    # Arrange & Act
    service = VectorIndexingService(chunk_size=200, chunk_overlap=50)

    # Assert
    assert service.chunk_size == 200
    assert service.chunk_overlap == 50
    assert service.splitter is not None