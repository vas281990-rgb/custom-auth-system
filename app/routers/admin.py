from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.role import Role
from app.models.audit_log import AuditLog
from app.api.deps import require_permission, get_pagination_params
from app.core.security import get_current_user
from app.services.audit import log_event

from app.schemas.pagination import PaginatedResponse
from app.schemas.user import UserRead
from app.schemas.role import RoleRead
from app.schemas.audit import AuditLogRead 

router = APIRouter(prefix="/admin", tags=["Admin (RBAC Management)"])


@router.get(
     "/roles",
    response_model=PaginatedResponse[RoleRead], 
    dependencies=[Depends(require_permission("users:update"))]
)
def list_roles(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
):
    """Fetch all available roles with pagination"""
    # 1. Prepare the query
    query = db.query(Role)
    
    # 2. Get the total count for the frontend
    total_count = query.count()

    # 3. Get the slice of data
    roles = query.offset(pagination["offset"]).limit(pagination["limit"]).all()

    # 4. Format roles to match RoleRead schema (extracting permission names)
    formatted_roles = []
    for r in roles:
        formatted_roles.append({
        "id": r.id,
        "name": r.name,
        "description": r.description,
        "permissions": [p.name for p in r.permissions]
    })

    return {
        "items": formatted_roles,
        "total": total_count,
        "limit": pagination["limit"],
        "offset": pagination["offset"]
        }


@router.post("/users/{user_id}/assign-role/{role_id}", dependencies=[Depends(require_permission("users:update"))])
def assign_role_to_user(
    user_id: int, 
    role_id: int, 
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    """Assign a specific role to a user and log the action"""
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
    
    # Check if the user already has this role to prevent duplicates
    if role not in user.roles:
        user.roles.append(role)
        db.commit()

        #Logging action
        log_event(
            db=db,
            user_id=current_user.id,
            action="assign_role",
            details=f"Admin {current_user.email} assigned role {role.name} to user {user.email}",
            ip_address=request.client.host
        )
    
    return {"message": f"Role {role.name} assigned to user {user.email}"}

@router.get(
    "/users", 
    response_model=PaginatedResponse[UserRead],
    dependencies=[Depends(require_permission("users:read"))]
)
def list_users(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
):
    """Retrieve a paginated list of all non-deleted users"""
    
    query = db.query(User).filter(User.is_deleted == False)
    
    # Calculate the total count of users matching the criteria
    total_count = query.count()

    # Apply pagination: skip 'offset' rows and take 'limit' rows (data slice)
    users = query.offset(pagination["offset"])\
        .limit(pagination["limit"])\
        .all()
    
    # Return structured paginated response
    return{
        "items": users,
        "total": total_count,
        "limit": pagination["limit"],
        "offset": pagination["offset"]
    }

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permission("users:delete"))])
def delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soft-delete a user and log the action"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_deleted = True
    db.commit()

    # LOGGING ACTION
    log_event(
        db=db,
        user_id=current_user.id,
        action="delete_user",
        details=f"Admin {current_user.email} soft-deleted user {user.email}",
        ip_address=request.client.host
    )
    return None

@router.get(
    "/audit-logs", 
    response_model=PaginatedResponse[AuditLogRead],
    dependencies=[Depends(require_permission("users:read"))]
)
def list_audit_logs(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params)
):
    """View all audit logs (Admin only)"""
    query = db.query(AuditLog) 
    total_count = query.count()
    
    # sorting by date
    from sqlalchemy import desc
    logs = query.order_by(desc(AuditLog.created_at))\
                .offset(pagination["offset"])\
                .limit(pagination["limit"])\
                .all()
    
    return {
        "items": logs,
        "total": total_count,
        "limit": pagination["limit"],
        "offset": pagination["offset"]
    }