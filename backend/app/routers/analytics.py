from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.middleware.auth import require_admin
from app.models.user import User
from app.services.analytics_service import get_dashboard_metrics

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/dashboard")
async def get_dashboard_stats(
    session: AsyncSession = Depends(get_session),
    _admin: User = Depends(require_admin),
):
    """Get overall platform metrics (admin only)."""
    return await get_dashboard_metrics(session)
