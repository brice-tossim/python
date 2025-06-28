import logging
from typing import List, Optional

from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

logger = logging.getLogger(__name__)


class VectorIndexingService:
    """
    Service to create and manage vector indexes from documents
    """

    def __init__(
        self,
        chunk_size: int = 150,
        chunk_overlap: int = 40,
    ) -> None:
        """
        Initialize the vector indexing service

        Args:
            chunk_size (int): Size of chunks to split the document into
            chunk_overlap (int): Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Configure the sentence splitter
        self.splitter = SentenceSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

    def create_index_from_documents(
        self, documents: List[Document]
    ) -> Optional[VectorStoreIndex]:
        """
        Create a vector index from the given documents

        Args:
            documents (List[Document]): List of documents to create the index from

        Returns:
            VectorStoreIndex: The created vector index
        """
        if not documents:
            logger.warning("No documents provided for creating vector index.")
            return None

        try:
            logger.info(f"Creating vector index with {len(documents)} nodes.")

            # Split the documents into smaller nodes/chunks
            nodes = self.splitter.get_nodes_from_documents(documents)

            # Create the vector index
            index = VectorStoreIndex(nodes)

            logger.info("Vector index created successfully.")
            return index
        except Exception as e:
            logger.error(f"Error creating vector index: {e}")
            return None
