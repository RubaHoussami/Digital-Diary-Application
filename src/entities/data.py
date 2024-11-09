from pydantic import BaseModel, Field


class Data(BaseModel):
    id: int = Field(..., description="The id of the data")
    mistake_ratio: float = Field(..., description="The mistake ratio of the data")
    original_text: str = Field(..., description="The original text provided by the user")
    sanitized_text: str = Field(..., description="The sanitized text of the data")
    tokens: list[str] = Field(..., description="The tokens of the sanitized text")
