from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Schema for chat request
    """

    query: str = Field(
        description="The query to be processed by the chat service.",
        min_length=1,
    )
