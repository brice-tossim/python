import logging
from typing import Optional, List

from llama_index.core import VectorStoreIndex
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata

from api.config.llm_config import LLMConfig

logger = logging.getLogger(__name__)


class ReActAgentService:
    """
    Service to handle user queries using ReAct agent with Wikipedia tool
    """

    def __init__(
        self,
        max_iterations: int = 10,
    ) -> None:
        """
        Initialize the ReAct Agent Service

        Args:
            max_iterations (int): Maximum number of iterations for ReAct agent
        """
        self.max_iterations = max_iterations

        # Initialize the ReAct agent (the agent will be created once the tools are available)
        self.agent: Optional[ReActAgent] = None
        self.tools: List[QueryEngineTool] = []

    def initialize_agent(self, tools: List[QueryEngineTool]) -> None:
        """
        Initialize the ReAct agent with the given tools

        Args:
            tools (List[QueryEngineTool]): List of tools to use for the agent
        """
        try:
            logger.info("Initializing ReAct agent.")

            self.tools = tools

            # Initialize the OpenAI LLM
            llm = LLMConfig.get_llm()

            # Create the ReAct agent
            self.agent = ReActAgent.from_tools(
                tools=self.tools,
                llm=llm,
                max_iterations=self.max_iterations,
                system_prompt=self._get_system_prompt(),
                verbose=True,
            )

            logger.info("ReAct agent initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing ReAct agent: {e}")
            raise RuntimeError(f"Error initializing ReAct agent: {e}")

    def query(self, user_query: str) -> str:
        """
        Query the ReAct agent with the given user query

        Args:
            user_query (str): User query to query the agent with

        Returns:
            str: Response from the agent
        """
        if not self.agent:
            raise RuntimeError("ReAct agent is not initialized.")

        user_query = user_query.strip()
        if not user_query:
            return "I need a question to help you. Please ask me something."

        try:
            logger.info("Querying ReAct agent.")

            # Query the agent
            response = self.agent.chat(user_query)

            logger.info("ReAct agent queried successfully.")
            return str(response)
        except Exception as e:
            logger.error(f"Error querying ReAct agent: {e}")
            raise RuntimeError(f"Error querying ReAct agent: {e}")

    @staticmethod
    def create_wikipedia_tool(
        index: VectorStoreIndex,
        similarity_top_k: int = 5,
        response_mode: str = "compact",
    ) -> QueryEngineTool:
        """
        Create the Wikipedia query engine tool from the given index

        Args:
            index (VectorStoreIndex): Vector store index containing Wikipedia content
            similarity_top_k (int): Number of similar Wikipedia pages to retrieve
            response_mode (str): Response mode for Wikipedia tool

        Returns:
            QueryEngineTool: Wikipedia tool
        """
        try:
            logger.info("Creating Wikipedia query engine tool.")

            # Create the Wikipedia query engine tool
            query_engine = index.as_query_engine(
                response_mode=response_mode,
                similarity_top_k=similarity_top_k,
                verbose=True,
            )

            # Create tool metadata
            tool_metadata = ToolMetadata(
                name="wikipedia_search",
                description="Useful for when you need to answer questions about Wikipedia.",
            )

            # Create the Wikipedia query engine tool
            wikipedia_tool = QueryEngineTool(
                query_engine=query_engine,
                metadata=tool_metadata,
            )

            logger.info("Wikipedia query engine tool created successfully.")
            return wikipedia_tool
        except Exception as e:
            logger.error(f"Error creating Wikipedia query engine tool: {e}")
            raise RuntimeError(f"Error creating Wikipedia query engine tool: {e}")

    @staticmethod
    def _get_system_prompt() -> str:
        """
        Get the system prompt for the ReAct agent

        Returns:
            str: System prompt
        """
        return """
        You are a helpful AI assistant with access to Wikipedia information. 

        Your role is to:
        1. Understand user questions and determine if you need to search for information
        2. Use the wikipedia_search tool when you need factual information
        3. Provide accurate, helpful responses based on the retrieved information
        4. Cite your sources when providing information from Wikipedia
        5. If you cannot find relevant information, clearly state that

        Guidelines:
        - Always use the tool when you need to look up factual information
        - Be concise but comprehensive in your responses
        - If the retrieved information doesn't fully answer the question, say so
        - Provide context and explanations, not just raw facts
        - If asked about recent events beyond your knowledge, acknowledge limitations

        Remember: You have access to Wikipedia content through the search tool. Use it wisely!
        """
