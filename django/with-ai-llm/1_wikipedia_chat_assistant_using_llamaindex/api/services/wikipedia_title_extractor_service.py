from typing import List

from llama_index.program.openai import OpenAIPydanticProgram

from api.config.llm_config import LLMConfig
from api.schemas.wikipedia_title_extraction import WikipediaTitleExtraction


class WikipediaTitleExtractorService:
    """
    Service to extract titles from user query using OpenAI
    """

    def __init__(self) -> None:
        self._program = self._create_extraction_program()

    def extract_titles(self, query: str) -> List[str]:
        """
        Extract Wikipedia titles from the user query

        Args:
            query (str): User query to extract titles from

        Returns:
            WikipediaTitleExtraction: Extracted titles
        """
        result = self._program(query=query)
        if isinstance(result, WikipediaTitleExtraction):
            return result.titles

        return []

    @staticmethod
    def _create_extraction_program() -> OpenAIPydanticProgram:
        """
        Create a program to extract titles from user input using OpenAI

        Returns:
            OpenAIPydanticProgram: Program for extracting Wikipedia titles
        """

        prompt_template_str = """
        You are a Wikipedia research assistant. Your task is to analyze the user's query and identify exactly 5 relevant Wikipedia page titles that would contain information to help answer their question.

        INSTRUCTIONS:
        1. Extract exactly 5 Wikipedia page titles (no more, no less)
        2. Use exact Wikipedia page titles (proper capitalization and formatting)
        3. Focus on the most relevant and specific topics first
        4. Include broader context topics if needed to reach 5 titles
        5. If the query has insufficient information for 5 relevant titles, return an empty array []

        GUIDELINES:
        - Prioritize main subjects, entities, concepts, events, or people mentioned
        - Include related topics that provide essential context
        - Use standard Wikipedia naming conventions (e.g., "World War II" not "WWII")
        - Avoid overly specific subtopics that might not have dedicated Wikipedia pages
        - Consider historical, scientific, geographical, or biographical pages as appropriate

        USER QUERY: {query}

        Return your response as a JSON array of exactly 5 strings (Wikipedia titles), or an empty array [] if insufficient relevant content can be identified.

        Examples:
        - Query: "What is the capital of France?" → ["Paris", "France", "Geography of France", "History of Paris", "French culture"]
        - Query: "How does photosynthesis work?" → ["Photosynthesis", "Chlorophyll", "Carbon dioxide", "Cellular respiration", "Plant"]
        - Query: "Random gibberish xyz123" → []

        Response format: ["Title 1", "Title 2", "Title 3", "Title 4", "Title 5"] or []
        """
        llm = LLMConfig.get_llm()

        return OpenAIPydanticProgram.from_defaults(
            output_cls=WikipediaTitleExtraction,
            prompt_template_str=prompt_template_str,
            llm=llm,
        )
