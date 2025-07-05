import logging
from typing import List

import wikipedia
from llama_index.core.schema import Document
from llama_index.readers.wikipedia import WikipediaReader

logger = logging.getLogger(__name__)


class WikipediaContentService:
    """
    Service to fetch and process Wikipedia content from titles using the WikipediaReader.
    """

    def __init__(self) -> None:
        self.reader = WikipediaReader()

    def fetch_content(self, titles: List[str]) -> List[Document]:
        """
        Fetch content from Wikipedia for the given titles.

        Args:
            titles (List[str]): List of Wikipedia page titles to fetch content for.

        Returns:
            List[Document]: List of Document objects containing the fetched content.
        """
        if not titles:
            logger.warning("No titles provided for fetching content from Wikipedia.")
            return []

        try:
            logger.info(f"Fetching content from Wikipedia for {len(titles)} pages.")

            # Fetch the content from Wikipedia (disable auto-suggestion to avoid errors -- OpenAI already returns the best match)
            titles = self.validate_titles(titles)
            documents = self.reader.load_data(pages=titles, auto_suggest=False)
            return documents
        except Exception as e:
            logger.error(f"Error fetching content from Wikipedia: {e}")
            return []

    @staticmethod
    def validate_titles(titles: List[str]) -> List[str]:
        """
        Validate the given Wikipedia page titles to ensure they are valid.

        Args:
            titles (List[str]): List of Wikipedia page titles to correct.

        Returns:
            List[str]: List of corrected Wikipedia page titles.
        """
        try:
            logger.info(f"Correcting Wikipedia page titles for {len(titles)} pages.")

            # Correct Wikipedia page titles using the Wikipedia API
            corrected_titles = [wikipedia.search(t, results=1) for t in titles]
            return corrected_titles
        except Exception as e:
            logger.error(f"Error correcting Wikipedia page titles: {e}")
            return []