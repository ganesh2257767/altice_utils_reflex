from datetime import datetime, timezone
import reflex as rx
from sqlmodel import Field

class UserModel(rx.Model, table=True):
    __tablename__ = "users"
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    password: str
    role: str = Field(nullable=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )