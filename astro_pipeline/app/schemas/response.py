from pydantic import BaseModel

class PredictionResponse(BaseModel):
    zodiac: str
    insight: str
    language: str
    context_used: list[str] = [] # Debug info to see what RAG retrieved
