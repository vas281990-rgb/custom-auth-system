from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

def log_event(
    db: Session,
    action: str,
    user_id: int = None,
    details: str = None,
    ip_address: str = None
):
    """
    Creates a new audit log entry in the database.
    """
    new_log = AuditLog(
        user_id=user_id,
        action=action,
        details=details,
        ip_address=ip_address
    )
    db.add(new_log)
    db.commit() 