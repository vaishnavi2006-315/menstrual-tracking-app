from dataclasses import dataclass
from datetime import date, datetime
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.user import User


@dataclass(frozen=True)
class CycleRecord:
    start_date: date
    cycle_length: int


class CycleData(Base):
    __tablename__ = "cycle_data"
    __table_args__ = (
        CheckConstraint("cycle_length > 0", name="cycle_length_positive"),
        CheckConstraint(
            "(period_end_date IS NULL) OR (period_end_date >= period_start_date)", name="end_after_start"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="cycles")

    period_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    period_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    cycle_length: Mapped[int] = mapped_column(Integer, nullable=False)
    symptoms: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
