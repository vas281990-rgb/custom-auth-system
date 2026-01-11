from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.role import Role
from app.api.deps import require_permission

router = APIRouter(prefix="/admin", tags=["Admin (RBAC Management)"])


@router.get("/roles", dependencies=[Depends(require_permission("users:update"))])
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "permissions": [p.name for p in r.permissions]
        } for r in roles
    ]


@router.post("/users/{user_id}/assign-role/{role_id}", dependencies=[Depends(require_permission("users:update"))])
def assign_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
    
    if role not in user.roles:
        user.roles.append(role)
        db.commit()
    
    return {"message": f"Role {role.name} assigned to user {user.email}"}