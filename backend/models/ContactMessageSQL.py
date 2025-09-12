"""
ContactMessage PostgreSQL Model
DataLab Georgia - Migration from MongoDB to PostgreSQL
"""

from sqlalchemy import Column, String, Text, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ContactMessageSQL(Base):
    """PostgreSQL ORM model for contact messages"""
    __tablename__ = "contact_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default='new')
    
    # Add constraints
    __table_args__ = (
        CheckConstraint('status IN (\'new\', \'read\', \'replied\')', name='check_status'),
    )

# Pydantic models for API
class ContactMessageCreate(BaseModel):
    name: str = Field(..., max_length=100)
    email: str = Field(..., max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    subject: str = Field(..., max_length=200)
    message: str

class ContactMessageUpdate(BaseModel):
    status: Optional[str] = Field(None, regex=r'^(new|read|replied)$')

class ContactMessageResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    subject: str
    message: str
    created_at: datetime
    status: str
    
    class Config:
        from_attributes = True