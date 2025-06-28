from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from api.requests.chat import ChatRequest
from api.services.wikipedia_rag_service import WikipediaRagService
from api.services.wikipedia_title_extractor_service import (
    WikipediaTitleExtractorService,
)


class ChatView(APIView):
    """
    Handles user requests to answer queries from Wikipedia.
    """

    def post(self, request: Request) -> Response:
        """
        This method gets query from the request and returns a response based on the query.

        Args:
            request (Request): The incoming request containing the query.

        Returns:
            Response: A response containing the result of the query processing.
        """
        data = request.data if isinstance(request.data, dict) else {}
        query = data.get("query", "")
        if query == "":
            return Response({"error": '"query" parameter is required'}, status=400)

        rag_service = WikipediaRagService()
        response = rag_service.query(query)
        return Response({"response": response})
