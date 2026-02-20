from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class CyclePredictionRequest(BaseModel):
    last_period_start: date
    history: list[int] = Field(default_factory=list)
    average_cycle_length: Optional[int] = None


class CyclePredictionResponse(BaseModel):
    next_period_start: date
    cycle_length: int
    confidence: float
