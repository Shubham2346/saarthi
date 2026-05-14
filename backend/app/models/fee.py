import uuid
import enum
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Enum as SAEnum

if TYPE_CHECKING:
    from app.models.user import User

class FeeStatus(str, enum.Enum):
    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    OVERDUE = "overdue"

class FeeRecord(SQLModel, table=True):
    """Tracks student financial obligations and payments."""
    __tablename__ = "fee_records"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    
    fee_type: str = Field(max_length=100) # e.g., "Tuition", "Hostel", "Library"
    total_amount: float = Field(default=0.0)
    paid_amount: float = Field(default=0.0)
    
    status: FeeStatus = Field(
        default=FeeStatus.PENDING,
        sa_column=Column(SAEnum(FeeStatus), nullable=False, default=FeeStatus.PENDING)
    )
    
    due_date: datetime
    last_payment_date: Optional[datetime] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="fee_records")
