from datetime import date, datetime
from pydantic import BaseModel, Field, conint, constr, model_validator


class CycleDataBase(BaseModel):
    user_id: int
    period_start_date: date
    period_end_date: date | None = None
    cycle_length: conint(gt=0)
    symptoms: constr(max_length=255) | None = Field(default=None)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.period_end_date is not None and self.period_end_date < self.period_start_date:
            raise ValueError("period_end_date must be >= period_start_date")
        return self


class CycleDataCreate(CycleDataBase):
    pass


class CycleDataResponse(CycleDataBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
