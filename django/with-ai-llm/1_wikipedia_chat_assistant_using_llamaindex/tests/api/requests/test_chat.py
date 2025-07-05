import pytest
from pydantic_core import ValidationError

from api.requests.chat import ChatRequest


def test_chat_request_valid():
    req = ChatRequest(query="Test query")
    assert req.query == "Test query"

def test_chat_request_invalid():
    with pytest.raises(ValidationError):
        ChatRequest(query="")