import reflex as rx
from datetime import datetime, timezone
from sqlmodel import Field


class ContactModel(rx.Model, table=True):
    __tablename__ = "contact"
    created_by: str = Field(foreign_key="users.email", nullable=False)
    message: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
