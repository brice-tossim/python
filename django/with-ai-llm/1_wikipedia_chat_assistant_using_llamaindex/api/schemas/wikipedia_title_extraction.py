from typing import List

from pydantic import BaseModel, Field


class WikipediaTitleExtraction(BaseModel):
    """
    Schema for extracting Wikipedia titles from user input
    """
    titles: List[str] = Field(
        default_factory=list,
        description="List of Wikipedia page titles extracted from the user query"
    )
    
    class ConfigDict:
        json_schema_extra = {
            "example": {
                "titles": ["Python (programming language)", "Django (web framework)"]
            }
        }
