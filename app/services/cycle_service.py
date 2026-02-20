from datetime import timedelta
from statistics import mean
from app.schemas.cycle import CyclePredictionRequest, CyclePredictionResponse


def predict_next_period(request: CyclePredictionRequest) -> CyclePredictionResponse:
    hist = request.history or []
    cycle_length = request.average_cycle_length or (int(mean(hist)) if hist else 28)
    cycle_length = max(20, min(cycle_length, 45))
    confidence = 0.5 if not hist else min(0.95, 0.6 + 0.05 * len(hist))
    next_period_start = request.last_period_start + timedelta(days=cycle_length)
    return CyclePredictionResponse(
        next_period_start=next_period_start, cycle_length=cycle_length, confidence=confidence
    )
