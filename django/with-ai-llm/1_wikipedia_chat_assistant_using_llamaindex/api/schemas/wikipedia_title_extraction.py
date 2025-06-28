from typing import List
from pydantic import BaseModel


class WikipediaTitleExtraction(BaseModel):
    """
    Schema for extracting wikipedia titles from user input
    """

    titles: List[str] = []
