import uuid
from datetime import datetime, timezone
from typing import Optional, Any
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column

class AuditLog(SQLModel, table=True):
    """Immutable audit trails for compliance and traceability."""
    __tablename__ = "audit_logs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    actor_id: Optional[uuid.UUID] = Field(default=None, index=True) # Who performed the action
    target_id: Optional[uuid.UUID] = Field(default=None, index=True) # Who/What was affected
    
    action: str = Field(max_length=100, index=True) # e.g., "DOCUMENT_VERIFIED", "ROLE_UPDATED"
    entity_type: str = Field(max_length=50) # e.g., "User", "Document", "Task"
    
    # Store state transitions or metadata
    old_value: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    new_value: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    
    ip_address: Optional[str] = Field(default=None, max_length=50)
    
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
