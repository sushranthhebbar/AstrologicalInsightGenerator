from pydantic import BaseModel, Field, validator
from datetime import date as date_type

class PredictionRequest(BaseModel):
    name: str = Field(..., example="Ritika")
    birth_date: str = Field(..., example="1995-08-20")
    birth_time: str = Field(..., example="14:30")
    birth_place: str = Field(..., example="Jaipur, India")
    language: str = Field("en", example="en", description="Target language code (e.g., 'en', 'hi')")

    @validator("birth_date")
    def validate_date(cls, v):
        try:
            # Simple check to ensure YYYY-MM-DD format
            date_type.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
