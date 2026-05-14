"""
Conversation service — manages chat session persistence and turn tracking.
"""

import uuid
from typing import Optional
from datetime import datetime, timezone

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation


class ConversationService:
    """Service for creating and updating conversation records."""

    async def get_or_create(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        conversation_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Conversation:
        """Get existing conversation by ID or session, or create a new one."""
        if conversation_id:
            try:
                conv_uuid = uuid.UUID(conversation_id)
                conv = await session.get(Conversation, conv_uuid)
                if conv:
                    return conv
            except ValueError:
                pass

        if session_id:
            statement = select(Conversation).where(
                Conversation.session_id == session_id,
                Conversation.user_id == user_id,
            ).order_by(Conversation.created_at.desc()).limit(1)
            result = await session.execute(statement)
            conv = result.scalar_one_or_none()
            if conv:
                return conv

        conv = Conversation(
            user_id=user_id,
            session_id=session_id or str(uuid.uuid4()),
            turn_count=0,
        )
        session.add(conv)
        await session.flush()
        await session.refresh(conv)
        return conv

    async def increment_turn(
        self, session: AsyncSession, conversation: Conversation
    ) -> Conversation:
        """Increment turn count and update timestamp."""
        conversation.turn_count += 1
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        await session.flush()
        await session.refresh(conversation)
        return conversation

    async def update_metadata(
        self,
        session: AsyncSession,
        conversation: Conversation,
        intent_summary: Optional[str] = None,
        agent_sequence: Optional[str] = None,
        was_escalated: bool = False,
        escalation_reason: Optional[str] = None,
    ) -> Conversation:
        """Update conversation metadata after agent processing."""
        if intent_summary is not None:
            conversation.intent_summary = intent_summary
        if agent_sequence is not None:
            conversation.agent_sequence = agent_sequence
        if was_escalated:
            conversation.was_escalated = True
        if escalation_reason is not None:
            conversation.escalation_reason = escalation_reason
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        await session.flush()
        await session.refresh(conversation)
        return conversation

    async def get_user_conversations(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        limit: int = 20,
    ) -> list[Conversation]:
        """Get recent conversations for a user."""
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
        )
        result = await session.execute(statement)
        return list(result.scalars().all())


# Singleton
conversation_service = ConversationService()
