import reflex as rx
from datetime import datetime, timezone
from sqlmodel import Field


class ContactModel(rx.Model, table=True):
    __tablename__ = "contact"
    created_by: int = Field(default=None, foreign_key="users.id")
    message: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
