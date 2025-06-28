import logging

from api.services.react_agent_service import ReActAgentService
from api.services.vector_indexing_service import VectorIndexingService
from api.services.wikipedia_content_service import WikipediaContentService
from api.services.wikipedia_title_extractor_service import (
    WikipediaTitleExtractorService,
)

logger = logging.getLogger(__name__)


class WikipediaRagService:
    """
    Service to handle user queries using Wikipedia RAG
    """

    def __init__(self) -> None:
        self.title_extractor = WikipediaTitleExtractorService()
        self.content_fetcher = WikipediaContentService()
        self.vector_indexer = VectorIndexingService()
        self.agent_service = ReActAgentService()
        self._is_agent_initialized = False

    def create_agent(self, user_query: str) -> None:
        """
        Create an agent for the given user query

        Args:
            user_query (str): User query to create the agent for

        Raises:
            RuntimeError: If there is an error creating the agent
        """
        try:
            logger.info("Creating Wikipedia RAG agent.")

            # Extract Wikipedia titles from the user query
            titles = self.title_extractor.extract_titles(user_query)
            if not titles:
                raise RuntimeError(
                    """
                    No relevant Wikipedia pages found for the given user query.
                    Please provide a more specific query.
                    """
                )

            # Fetch content from Wikipedia
            documents = self.content_fetcher.fetch_content(titles)
            if not documents:
                raise RuntimeError(
                    """
                    Failed to fetch content from Wikipedia.
                    The pages might not exist or might be private.
                    """
                )

            # Create a vector index from the Wikipedia content
            index = self.vector_indexer.create_index_from_documents(documents)
            if not index:
                raise RuntimeError(
                    """
                    Failed to create vector index from the fetched Wikipedia content.
                    The content might be invalid or insufficient.
                    """
                )

            # Create the Wikipedia tool and initialize the agent
            tool = self.agent_service.create_wikipedia_tool(index)
            self.agent_service.initialize_agent([tool])
            self._is_agent_initialized = True
        except Exception as e:
            logger.error(f"Error creating Wikipedia RAG agent: {e}")
            raise RuntimeError(f"Error creating Wikipedia RAG agent: {e}")

    def query(self, user_query: str) -> str:
        """
        Query the agent with the given user query

        Args:
            user_query (str): User query to query the agent with

        Returns:
            str: Response from the agent
        """
        try:
            if not self._is_agent_initialized:
                self.create_agent(user_query)

            return self.agent_service.query(user_query)
        except RuntimeError as e:
            logger.error(f"Query processing failed: {e}")
            return """
                I'm sorry, I couldn't process your query. This might be because:
                1. There are no relevant Wikipedia pages for the given query.
                2. The Wikipedia content is not sufficient to answer the query.
                Please try again with a more specific query.
                """
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return "An unexpected error occurred. Please try again later."
