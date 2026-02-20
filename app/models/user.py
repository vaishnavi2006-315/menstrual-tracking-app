from __future__ import annotations
import re
from datetime import datetime
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Integer,
    MetaData,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates


metadata = MetaData(
    naming_convention={
        "ix": "ix_%(table_name)s_%(column_0_N_name)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class Base(DeclarativeBase):
    metadata = metadata


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
