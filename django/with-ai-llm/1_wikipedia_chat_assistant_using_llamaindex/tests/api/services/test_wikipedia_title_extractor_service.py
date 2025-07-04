from unittest.mock import patch, MagicMock

from api.services.wikipedia_title_extractor_service import WikipediaTitleExtractorService


@patch("api.services.wikipedia_title_extractor_service.FunctionCallingProgram")
def test_extract_titles_returns_titles(mock_program_cls):
    # Arrange
    mock_program = MagicMock()
    mock_result = {"titles": ["A", "B", "C"]}
    mock_program.return_value = mock_result
    mock_program_cls.from_defaults.return_value = mock_program
    service = WikipediaTitleExtractorService()

    # Act
    result = service.extract_titles("test query")

    # Assert
    assert result == ["A", "B", "C"]
    mock_program.assert_called_once_with(query="test query")


@patch("api.services.wikipedia_title_extractor_service.FunctionCallingProgram")
def test_extract_titles_returns_empty_when_no_result(mock_program_cls):
    # Arrange
    mock_program = MagicMock()
    mock_program.return_value = None
    mock_program_cls.from_defaults.return_value = mock_program
    service = WikipediaTitleExtractorService()

    # Act
    result = service.extract_titles("test query")

    # Assert
    assert result == []
    mock_program.assert_called_once_with(query="test query")


@patch('api.services.wikipedia_title_extractor_service.WikipediaTitleExtraction')
@patch('api.services.wikipedia_title_extractor_service.FunctionCallingProgram')
def test_extract_titles_handles_validation_error(mock_program_cls, mock_wte):
    # First, create the service with a mock program
    mock_program = MagicMock()
    mock_program.return_value = {"titles": ["invalid"]}  # This will cause a validation error
    mock_program_cls.from_defaults.return_value = mock_program

    # Make the validation raise an exception
    mock_wte.side_effect = Exception("Validation error")

    service = WikipediaTitleExtractorService()

    # This should be caught by the try/except in extract_titles
    result = service.extract_titles("test query")

    # Should return an empty list on validation error
    assert result == []
    mock_program.assert_called_once_with(query="test query")
