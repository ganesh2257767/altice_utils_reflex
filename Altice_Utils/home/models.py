from datetime import datetime, timezone
from sqlmodel import Field

import reflex as rx

class UsageModel(rx.Model, table=True):
    __tablename__ = "usages"
    used_by: str = Field(foreign_key="users.email", nullable=False)
    service_used: str
    used_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
