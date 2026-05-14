"""
Audit logging service — records all significant actions for security and compliance.
"""

import uuid
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc

from app.models.audit_log import AuditLog


class AuditService:
    """Centralized audit logging for all user actions."""

    async def log(
        self,
        session: AsyncSession,
        action: str,
        resource: str,
        user_id: Optional[uuid.UUID] = None,
        user_email: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        success: bool = True,
    ) -> AuditLog:
        entry = AuditLog(
            user_id=user_id,
            user_email=user_email,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=json.dumps(details) if details else None,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
        )
        session.add(entry)
        return entry

    async def get_logs(
        self,
        session: AsyncSession,
        user_id: Optional[uuid.UUID] = None,
        action: Optional[str] = None,
        resource: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AuditLog]:
        query = select(AuditLog).order_by(desc(AuditLog.created_at))

        if user_id:
            query = query.where(AuditLog.user_id == user_id)
        if action:
            query = query.where(AuditLog.action == action)
        if resource:
            query = query.where(AuditLog.resource == resource)

        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_recent_actions(
        self,
        session: AsyncSession,
        limit: int = 50,
    ) -> List[AuditLog]:
        query = select(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())


audit_service = AuditService()
