from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, conint, constr


class UserBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=100)
    email: EmailStr
    age: conint(ge=0, le=150) = Field(default=0)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
