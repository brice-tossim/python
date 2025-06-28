from typing import Optional

from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI


class LLMConfig:
    """
    Configuration class for LLM
    """

    _llm: Optional[OpenAI] = None
    _embedding_instance: Optional[OpenAIEmbedding] = None
    _is_llm_initialized: bool = False

    @classmethod
    def initialize(
        cls,
        model: str = "gpt-4o",
        temperature: float = 0.1,
        max_tokens: int = 1000,
        timeout: int = 60,
        embedding_model: str = "text-embedding-3-small",
        embed_batch_size: int = 100,
    ) -> None:
        """
        Initialize the LLM configuration

        Args:
            model (str): Model to use for OpenAI
            temperature (float): Temperature for OpenAI
            max_tokens (int): Maximum number of tokens for OpenAI
            timeout (int): Timeout for OpenAI
            embedding_model (str): Model to use for embeddings
            embed_batch_size (int): Batch size for embedding
        """
        cls.model = model
        cls.temperature = temperature
        cls.max_tokens = max_tokens
        cls.timeout = timeout
        cls.embedding_model = embedding_model
        cls.embed_batch_size = embed_batch_size

        # Initialize the OpenAI LLM
        cls._llm = OpenAI(
            model=cls.model,
            temperature=cls.temperature,
            max_tokens=cls.max_tokens,
            timeout=cls.timeout,
        )

        # Initialize the OpenAI embedding model
        cls._embedding_model = OpenAIEmbedding(
            model=cls.embedding_model,
            embed_batch_size=cls.embed_batch_size,
        )

        # Set global settings
        Settings.llm = cls._llm
        Settings.embed_model = cls._embedding_model

        # Set initialization flag
        cls._is_llm_initialized = True

    @classmethod
    def get_llm(cls) -> OpenAI:
        """
        Get the OpenAI LLM instance

        Returns:
            OpenAI: OpenAI LLM instance
        """
        if not cls._is_llm_initialized:
            cls.initialize()

        return cls._llm

    @classmethod
    def get_embedding_model(cls) -> OpenAIEmbedding:
        """
        Get the OpenAI embedding model instance

        Returns:
            OpenAIEmbedding: OpenAI embedding model instance
        """
        if not cls._is_llm_initialized:
            cls.initialize()

        return cls._embedding_model
