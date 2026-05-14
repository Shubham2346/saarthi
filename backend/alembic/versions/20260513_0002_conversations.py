"""create conversations table

Revision ID: 20260513_0002
Revises: 20260513_0001
Create Date: 2026-05-13

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260513_0002"
down_revision: Union[str, None] = "20260513_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "conversations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("session_id", sa.String(length=255), nullable=False),
        sa.Column("turn_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("title", sa.String(length=500), nullable=True),
        sa.Column("intent_summary", sa.String(length=1000), nullable=True),
        sa.Column("agent_sequence", sa.Text(), nullable=True),
        sa.Column("was_escalated", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("escalation_reason", sa.String(length=1000), nullable=True),
        sa.Column("escalation_ticket_id", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_conversations_user_id",
        "conversations",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_conversations_session_id",
        "conversations",
        ["session_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_conversations_session_id", table_name="conversations")
    op.drop_index("ix_conversations_user_id", table_name="conversations")
    op.drop_table("conversations")
