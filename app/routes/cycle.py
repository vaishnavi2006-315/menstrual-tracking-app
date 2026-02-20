from fastapi import APIRouter
from app.schemas.cycle import CyclePredictionRequest, CyclePredictionResponse
from app.services.cycle_service import predict_next_period


router = APIRouter(prefix="/cycle", tags=["cycle"])


@router.post("/predict", response_model=CyclePredictionResponse)
async def predict(request: CyclePredictionRequest) -> CyclePredictionResponse:
    return predict_next_period(request)
