import uuid
from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role, Permission, RolePermission, UserRoleLink
from app.models.user import User, UserRole


PERMISSION_DEFINITIONS = [
    {"code": "admission.apply", "name": "Apply for admission", "resource": "admission", "action": "apply"},
    {"code": "admission.view", "name": "View admission details", "resource": "admission", "action": "view"},
    {"code": "admission.list_all", "name": "List all applications", "resource": "admission", "action": "list_all"},
    {"code": "admission.approve", "name": "Approve/reject admission", "resource": "admission", "action": "approve"},
    {"code": "documents.upload", "name": "Upload documents", "resource": "documents", "action": "upload"},
    {"code": "documents.verify", "name": "Verify documents", "resource": "documents", "action": "verify"},
    {"code": "documents.view_all", "name": "View all documents", "resource": "documents", "action": "view_all"},
    {"code": "users.view", "name": "View user profiles", "resource": "users", "action": "view"},
    {"code": "users.manage", "name": "Manage users", "resource": "users", "action": "manage"},
    {"code": "users.assign_mentor", "name": "Assign mentor to student", "resource": "users", "action": "assign_mentor"},
    {"code": "tasks.view", "name": "View tasks", "resource": "tasks", "action": "view"},
    {"code": "tasks.manage", "name": "Manage tasks", "resource": "tasks", "action": "manage"},
    {"code": "tasks.assign", "name": "Assign tasks to users", "resource": "tasks", "action": "assign"},
    {"code": "tickets.create", "name": "Create support tickets", "resource": "tickets", "action": "create"},
    {"code": "tickets.view", "name": "View support tickets", "resource": "tickets", "action": "view"},
    {"code": "tickets.manage", "name": "Manage all tickets", "resource": "tickets", "action": "manage"},
    {"code": "fees.view", "name": "View fee details", "resource": "fees", "action": "view"},
    {"code": "fees.manage", "name": "Manage fee structure", "resource": "fees", "action": "manage"},
    {"code": "knowledge.view", "name": "View knowledge base", "resource": "knowledge", "action": "view"},
    {"code": "knowledge.manage", "name": "Manage knowledge base", "resource": "knowledge", "action": "manage"},
    {"code": "mentor.view_assigned", "name": "View assigned students", "resource": "mentor", "action": "view_assigned"},
    {"code": "mentor.add_notes", "name": "Add mentor notes", "resource": "mentor", "action": "add_notes"},
    {"code": "mentor.schedule", "name": "Schedule meetings", "resource": "mentor", "action": "schedule"},
    {"code": "system.admin", "name": "Full system administration", "resource": "system", "action": "admin"},
    {"code": "system.settings", "name": "Manage system settings", "resource": "system", "action": "settings"},
    {"code": "system.audit", "name": "View audit logs", "resource": "system", "action": "audit"},
    {"code": "system.backup", "name": "Backup and restore", "resource": "system", "action": "backup"},
    {"code": "reports.generate", "name": "Generate reports", "resource": "reports", "action": "generate"},
    {"code": "announcements.send", "name": "Send announcements", "resource": "announcements", "action": "send"},
]

ROLE_PERMISSIONS_MAP = {
    "student": [
        "admission.apply", "admission.view",
        "documents.upload",
        "users.view",
        "tasks.view",
        "tickets.create", "tickets.view",
        "fees.view",
        "knowledge.view",
    ],
    "admin": [
        "admission.view", "admission.list_all", "admission.approve",
        "documents.verify", "documents.view_all",
        "users.view", "users.manage", "users.assign_mentor",
        "tasks.view", "tasks.manage", "tasks.assign",
        "tickets.view", "tickets.manage",
        "fees.view", "fees.manage",
        "knowledge.view", "knowledge.manage",
        "reports.generate",
        "announcements.send",
    ],
    "mentor": [
        "users.view",
        "tasks.view",
        "tickets.view",
        "knowledge.view",
        "mentor.view_assigned", "mentor.add_notes", "mentor.schedule",
    ],
    "system_admin": [
        "admission.list_all", "admission.approve",
        "documents.verify", "documents.view_all",
        "users.view", "users.manage", "users.assign_mentor",
        "tasks.manage", "tasks.assign",
        "tickets.manage",
        "fees.manage",
        "knowledge.manage",
        "system.admin", "system.settings", "system.audit", "system.backup",
        "reports.generate",
        "announcements.send",
    ],
    "department_coordinator": [
        "admission.view", "admission.list_all",
        "documents.view_all",
        "users.view",
        "tasks.view",
        "tickets.view", "tickets.manage",
        "knowledge.view", "knowledge.manage",
        "reports.generate",
    ],
}


async def seed_default_roles(session: AsyncSession):
    for role_name in ["student", "admin", "mentor", "system_admin", "department_coordinator"]:
        existing = await session.execute(select(Role).where(Role.name == role_name))
        if not existing.scalar_one_or_none():
            role = Role(
                name=role_name,
                description={
                    "student": "Admission applicant and student portal user",
                    "admin": "Handles admission operations",
                    "mentor": "Guides students after admission",
                    "system_admin": "Technical platform management",
                    "department_coordinator": "Department-level admission coordination",
                }.get(role_name, ""),
                is_system=(role_name == "system_admin"),
            )
            session.add(role)
    await session.flush()


async def seed_permissions(session: AsyncSession):
    for perm_def in PERMISSION_DEFINITIONS:
        existing = await session.execute(
            select(Permission).where(Permission.code == perm_def["code"])
        )
        if not existing.scalar_one_or_none():
            perm = Permission(**perm_def)
            session.add(perm)
    await session.flush()


async def seed_role_permissions(session: AsyncSession):
    roles_stmt = select(Role)
    roles_result = await session.execute(roles_stmt)
    roles = {r.name: r for r in roles_result.scalars().all()}

    perms_stmt = select(Permission)
    perms_result = await session.execute(perms_stmt)
    permissions = {p.code: p for p in perms_result.scalars().all()}

    for role_name, perm_codes in ROLE_PERMISSIONS_MAP.items():
        role = roles.get(role_name)
        if not role:
            continue
        for code in perm_codes:
            perm = permissions.get(code)
            if not perm:
                continue
            existing = await session.execute(
                select(RolePermission).where(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == perm.id,
                )
            )
            if not existing.scalar_one_or_none():
                session.add(RolePermission(role_id=role.id, permission_id=perm.id))
    await session.flush()


async def assign_role_to_user(session: AsyncSession, user: User, role_name: str):
    role_stmt = select(Role).where(Role.name == role_name)
    role_result = await session.execute(role_stmt)
    role = role_result.scalar_one_or_none()
    if not role:
        return
    existing = await session.execute(
        select(UserRoleLink).where(
            UserRoleLink.user_id == user.id,
            UserRoleLink.role_id == role.id,
        )
    )
    if not existing.scalar_one_or_none():
        session.add(UserRoleLink(user_id=user.id, role_id=role.id))
        user.role = UserRole(role_name) if role_name in ("student", "admin", "mentor") else user.role


async def get_user_permissions(session: AsyncSession, user_id: uuid.UUID) -> list[str]:
    stmt = (
        select(Permission.code)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(UserRoleLink, UserRoleLink.role_id == RolePermission.role_id)
        .where(UserRoleLink.user_id == user_id)
    )
    result = await session.execute(stmt)
    return [row[0] for row in result.all()]


async def user_has_permission(session: AsyncSession, user_id: uuid.UUID, permission_code: str) -> bool:
    permissions = await get_user_permissions(session, user_id)
    return permission_code in permissions


async def get_user_roles(session: AsyncSession, user_id: uuid.UUID) -> list[str]:
    stmt = (
        select(Role.name)
        .join(UserRoleLink, UserRoleLink.role_id == Role.id)
        .where(UserRoleLink.user_id == user_id)
    )
    result = await session.execute(stmt)
    return [row[0] for row in result.all()]
