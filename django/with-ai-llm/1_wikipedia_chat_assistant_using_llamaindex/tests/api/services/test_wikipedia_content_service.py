from unittest.mock import patch, MagicMock

from llama_index.core.schema import Document

from api.services.wikipedia_content_service import WikipediaContentService


def test_fetch_content_no_titles():
    # Arrange
    service = WikipediaContentService()

    # Act
    result = service.fetch_content([])

    # Assert
    assert result == []


@patch("api.services.wikipedia_content_service.WikipediaReader")
def test_fetch_content_success(mock_reader_cls):
    # Arrange
    mock_reader = MagicMock()
    mock_doc1 = Document(text="Content 1", metadata={"title": "Python"})
    mock_doc2 = Document(text="Content 2", metadata={"title": "Django"})
    mock_reader.load_data.return_value = [mock_doc1, mock_doc2]
    mock_reader_cls.return_value = mock_reader

    service = WikipediaContentService()
    service.reader = mock_reader

    test_titles = ["Python", "Django"]

    # Mock validate_titles to return the same titles
    with patch.object(service, "validate_titles", return_value=test_titles):
        # Act
        result = service.fetch_content(test_titles)

        # Assert
        assert len(result) == 2
        assert isinstance(result[0], Document)
        assert result[0].text == "Content 1"
        assert result[1].text == "Content 2"
        mock_reader.load_data.assert_called_once_with(pages=test_titles, auto_suggest=False)


@patch("api.services.wikipedia_content_service.WikipediaReader")
def test_fetch_content_handles_exception(mock_reader_cls):
    # Arrange
    mock_reader = MagicMock()
    mock_reader.load_data.side_effect = Exception("API Error")
    mock_reader_cls.return_value = mock_reader

    service = WikipediaContentService()
    service.reader = mock_reader

    # Act
    result = service.fetch_content(["Python"])

    # Assert
    assert result == []
    mock_reader.load_data.assert_called_once()


@patch("api.services.wikipedia_content_service.wikipedia.search")
def test_validate_titles_success(mock_search):
    # Arrange
    service = WikipediaContentService()
    test_titles = ["Python", "Django"]
    mock_search.side_effect = [
        ["Python (programming language)"],  # First call returns list with one result
        ["Django (web framework)"]  # Second call returns list with one result
    ]

    # Act
    result = service.validate_titles(test_titles)

    # Assert
    assert result == [["Python (programming language)"], ["Django (web framework)"]]
    assert mock_search.call_count == 2
    mock_search.assert_any_call("Python", results=1)
    mock_search.assert_any_call("Django", results=1)


@patch("api.services.wikipedia_content_service.wikipedia.search")
def test_validate_titles_with_empty_input(mock_search):
    # Arrange
    service = WikipediaContentService()

    # Act
    result = service.validate_titles([])

    # Assert
    assert result == []
    mock_search.assert_not_called()


@patch("api.services.wikipedia_content_service.wikipedia.search")
def test_validate_titles_handles_search_error(mock_search):
    # Arrange
    mock_search.side_effect = Exception("Search failed")
    service = WikipediaContentService()

    # Act
    result = service.validate_titles(["Python"])

    # Assert
    assert result == []
    mock_search.assert_called_once_with("Python", results=1)