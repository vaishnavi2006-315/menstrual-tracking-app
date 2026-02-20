from __future__ import annotations
import re
from datetime import datetime
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from app.core.database import Base


class User(Base):
    """
    User account model storing basic identity and profile attributes.
    Enforces uniqueness and format constraints for email, non-null name,
    bounded age, and automatic creation timestamp. Suitable for use in
    FastAPI, Flask, or any SQLAlchemy-powered application.
    """

    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("age >= 0 AND age <= 150", name="age_range"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    cycles: Mapped[list["CycleData"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    @validates("email")
    def validate_email(self, key: str, value: str) -> str:
        if value is None:
            raise ValueError("email cannot be null")
        v = value.strip()
        if len(v) == 0 or len(v) > 120:
            raise ValueError("email length must be between 1 and 120")
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("invalid email format")
        return v.lower()

    @validates("name")
    def validate_name(self, key: str, value: str) -> str:
        if value is None:
            raise ValueError("name cannot be null")
        v = value.strip()
        if len(v) == 0 or len(v) > 100:
            raise ValueError("name length must be between 1 and 100")
        return v

    @validates("age")
    def validate_age(self, key: str, value: int) -> int:
        if value is None:
            raise ValueError("age cannot be null")
        if not isinstance(value, int):
            raise ValueError("age must be an integer")
        if value < 0 or value > 150:
            raise ValueError("age must be between 0 and 150")
        return value

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, age={self.age!r})"
