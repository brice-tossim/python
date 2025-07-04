from pydantic_core import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.services.wikipedia_rag_service import WikipediaRagService
from api.requests.chat import ChatRequest


class ChatView(APIView):
    """
    Handles user requests to answer queries from Wikipedia.
    """

    def post(self, request: Request) -> Response:
        """
        This method gets "query" from the request, validates it using ChatRequest Pydantic model,
        and returns a response based on the query.

        Args:
            request (Request): The incoming request containing the query.

        Returns:
            Response: A response containing the result of the query processing or validation errors.
        """
        try:
            # Validate request data using Pydantic model
            chat_request = ChatRequest(**request.data)

            # Process the valid request
            rag_service = WikipediaRagService()
            response = rag_service.query(chat_request.query)
            return Response({"response": response})

        except ValidationError as e:
            # Format Pydantic validation errors to be more user-friendly
            errors = []
            for error in e.errors():
                field = ".".join(str(loc) for loc in error['loc'])
                msg = error['msg']
                if error['type'] == 'missing':
                    errors.append(f"Field '{field}' is required")
                else:
                    errors.append(f"{field} field: {msg}")

            return Response(
                {"error": "Validation error", "details": errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
