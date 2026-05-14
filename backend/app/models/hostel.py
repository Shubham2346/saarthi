import uuid
import enum
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Enum as SAEnum

if TYPE_CHECKING:
    from app.models.user import User

class AllocationStatus(str, enum.Enum):
    APPLIED = "applied"
    WAITLISTED = "waitlisted"
    ALLOCATED = "allocated"
    CHECKED_IN = "checked_in"
    REJECTED = "rejected"

class HostelAllocation(SQLModel, table=True):
    """Tracks student hostel applications and room assignments."""
    __tablename__ = "hostel_allocations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, unique=True)
    
    status: AllocationStatus = Field(
        default=AllocationStatus.APPLIED,
        sa_column=Column(SAEnum(AllocationStatus), nullable=False, default=AllocationStatus.APPLIED)
    )
    
    building_name: Optional[str] = Field(default=None, max_length=100)
    room_number: Optional[str] = Field(default=None, max_length=20)
    bed_identifier: Optional[str] = Field(default=None, max_length=20)
    
    check_in_date: Optional[datetime] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="hostel_allocation")
