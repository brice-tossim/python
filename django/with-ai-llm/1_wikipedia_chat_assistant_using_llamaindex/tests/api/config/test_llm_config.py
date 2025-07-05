import unittest
from unittest.mock import patch, MagicMock, ANY

from api.config.llm_config import LLMConfig


class TestLLMConfig(unittest.TestCase):
    def setUp(self):
        # Save original class variables
        self.original_llm = LLMConfig._llm
        self.original_embedding = LLMConfig._embedding_model
        self.original_initialized = LLMConfig._is_llm_initialized

        # Reset state before each test
        LLMConfig._llm = None
        LLMConfig._embedding_model = None
        LLMConfig._is_llm_initialized = False

    def tearDown(self):
        # Restore original class variables
        LLMConfig._llm = self.original_llm
        LLMConfig._embedding_model = self.original_embedding
        LLMConfig._is_llm_initialized = self.original_initialized

    def test_initialize(self):
        # Save original values
        original_llm = LLMConfig._llm
        original_embedding = LLMConfig._embedding_instance
        original_initialized = LLMConfig._is_llm_initialized

        try:
            # Create mocks
            mock_llm = MagicMock()
            mock_embedding = MagicMock()

            # Patch the class attributes
            with patch.object(LLMConfig, '_llm', mock_llm), \
                    patch.object(LLMConfig, '_embedding_instance', mock_embedding):

                # Act
                LLMConfig.initialize()

                # Assert
                self.assertTrue(LLMConfig._is_llm_initialized)
                self.assertIsNotNone(LLMConfig._llm)
                self.assertIsNotNone(LLMConfig._embedding_instance)

        finally:
            # Restore original values
            LLMConfig._llm = original_llm
            LLMConfig._embedding_instance = original_embedding
            LLMConfig._is_llm_initialized = original_initialized

    @patch('api.config.llm_config.LLMConfig.initialize')
    def test_get_llm_initializes_if_needed(self, mock_initialize):
        # Test when already initialized
        LLMConfig._is_llm_initialized = True
        LLMConfig._llm = MagicMock()

        result = LLMConfig.get_llm()
        mock_initialize.assert_not_called()
        self.assertEqual(result, LLMConfig._llm)

    @patch('api.config.llm_config.LLMConfig.initialize')
    def test_get_llm_calls_initialize_when_needed(self, mock_initialize):
        # Test when not initialized
        LLMConfig._is_llm_initialized = False
        LLMConfig._llm = None

        LLMConfig.get_llm()
        mock_initialize.assert_called_once()

    @patch('api.config.llm_config.LLMConfig.initialize')
    def test_get_embedding_model_returns_cached(self, mock_initialize):
        # Test when already initialized
        LLMConfig._is_llm_initialized = True
        LLMConfig._embedding_model = MagicMock()

        result = LLMConfig.get_embedding_model()
        mock_initialize.assert_not_called()
        self.assertEqual(result, LLMConfig._embedding_model)

    @patch('api.config.llm_config.LLMConfig.initialize')
    def test_get_embedding_model_calls_initialize_when_needed(self, mock_initialize):
        # Test when not initialized
        LLMConfig._is_llm_initialized = False
        LLMConfig._embedding_model = None

        LLMConfig.get_embedding_model()
        mock_initialize.assert_called_once()
