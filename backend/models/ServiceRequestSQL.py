"""
ServiceRequest PostgreSQL Model
DataLab Georgia - Migration from MongoDB to PostgreSQL
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Numeric, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ServiceRequestSQL(Base):
    """PostgreSQL ORM model for service requests"""
    __tablename__ = "service_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    device_type = Column(String(50), nullable=False)
    problem_description = Column(Text, nullable=False)
    urgency = Column(String(20), nullable=False)
    status = Column(String(20), default='pending')
    case_id = Column(String(20), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    estimated_completion = Column(DateTime(timezone=True), nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    is_read = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    approved_for_kanban = Column(Boolean, default=False)
    admin_comment = Column(Text, nullable=True)
    
    # Add constraints
    __table_args__ = (
        CheckConstraint('device_type IN (\'hdd\', \'ssd\', \'raid\', \'usb\', \'sd\', \'other\')', name='check_device_type'),
        CheckConstraint('urgency IN (\'low\', \'medium\', \'high\', \'critical\')', name='check_urgency'),
        CheckConstraint('status IN (\'pending\', \'in_progress\', \'completed\', \'picked_up\', \'archived\')', name='check_status'),
    )

# Pydantic models for API
class ServiceRequestCreate(BaseModel):
    name: str = Field(..., max_length=100)
    email: str = Field(..., max_length=255)
    phone: str = Field(..., max_length=20)
    device_type: str = Field(..., pattern=r'^(hdd|ssd|raid|usb|sd|other)$')
    problem_description: str
    urgency: str = Field(..., pattern=r'^(low|medium|high|critical)$')

class ServiceRequestUpdate(BaseModel):
    status: Optional[str] = Field(None, regex=r'^(pending|in_progress|completed|picked_up|archived)$')
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    price: Optional[float] = None
    is_read: Optional[bool] = None
    is_archived: Optional[bool] = None
    approved_for_kanban: Optional[bool] = None
    admin_comment: Optional[str] = None

class ServiceRequestResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    device_type: str
    problem_description: str
    urgency: str
    status: str
    case_id: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_completion: Optional[str] = None
    price: Optional[float] = None
    is_read: bool
    is_archived: bool
    approved_for_kanban: bool
    admin_comment: Optional[str] = None
    
    class Config:
        from_attributes = True