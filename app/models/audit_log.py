from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # User ID (can be empty if anonymous)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Actions: "login", "register", "assign_role", "delete_user"
    action = Column(String(50), nullable=False)
    
    # Details: "Admin assigned role manager to user test@example.com"
    details = Column(String(255), nullable=True)
    
    # Client's IP
    ip_address = Column(String(45), nullable=True)
    
    # Exact time
    created_at = Column(DateTime(timezone=True), server_default=func.now())
