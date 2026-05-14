import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, Text


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", index=True)
    user_email: Optional[str] = Field(default=None, max_length=255)
    action: str = Field(max_length=100, index=True)
    resource: str = Field(max_length=100)
    resource_id: Optional[str] = Field(default=None, max_length=100)
    details: Optional[str] = Field(default=None, sa_type=Text)
    ip_address: Optional[str] = Field(default=None, max_length=50)
    user_agent: Optional[str] = Field(default=None, max_length=500)
    success: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
