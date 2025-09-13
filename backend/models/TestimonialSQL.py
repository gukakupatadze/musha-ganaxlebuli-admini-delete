"""
Testimonial PostgreSQL Model
DataLab Georgia - Migration from MongoDB to PostgreSQL
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, CheckConstraint
from sqlalchemy.sql import func
from database import Base
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

class TestimonialSQL(Base):
    """PostgreSQL ORM model for testimonials"""
    __tablename__ = "testimonials"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    position_en = Column(String(100), nullable=False)
    text_ka = Column(Text, nullable=False)
    text_en = Column(Text, nullable=False)
    rating = Column(Integer, default=5)
    image = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Add constraints
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating'),
    )

# Pydantic models for API
class TestimonialCreate(BaseModel):
    name: str = Field(..., max_length=100)
    name_en: str = Field(..., max_length=100)
    position: str = Field(..., max_length=100)
    position_en: str = Field(..., max_length=100)
    text_ka: str
    text_en: str
    rating: int = Field(5, ge=1, le=5)
    image: Optional[str] = Field(None, max_length=500)
    
    @validator('image')
    def validate_image_url(cls, v):
        if v and not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('Image URL must start with http:// or https://')
        return v

class TestimonialUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    name_en: Optional[str] = Field(None, max_length=100)
    position: Optional[str] = Field(None, max_length=100)
    position_en: Optional[str] = Field(None, max_length=100)
    text_ka: Optional[str] = None
    text_en: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    image: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class TestimonialResponse(BaseModel):
    id: int
    name: str
    name_en: str
    position: str
    position_en: str
    text_ka: str
    text_en: str
    rating: int
    image: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True