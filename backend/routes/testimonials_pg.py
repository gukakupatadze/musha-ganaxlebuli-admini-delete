"""
Testimonials API Routes - PostgreSQL Version
DataLab Georgia - Migration from MongoDB to PostgreSQL
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, desc
from typing import List, Optional
import logging

from database import get_session
from models.TestimonialSQL import (
    TestimonialSQL,
    TestimonialCreate,
    TestimonialUpdate,
    TestimonialResponse
)

router = APIRouter()

@router.post("/", response_model=dict)
async def create_testimonial(
    testimonial: TestimonialCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new testimonial"""
    try:
        new_testimonial = TestimonialSQL(
            name=testimonial.name,
            name_en=testimonial.name_en,
            position=testimonial.position,
            position_en=testimonial.position_en,
            text_ka=testimonial.text_ka,
            text_en=testimonial.text_en,
            rating=testimonial.rating,
            image=testimonial.image
        )
        
        session.add(new_testimonial)
        await session.commit()
        await session.refresh(new_testimonial)
        
        return {
            "success": True,
            "message": "Testimonial created successfully",
            "id": str(new_testimonial.id)
        }
        
    except Exception as e:
        await session.rollback()
        logging.error(f"Error creating testimonial: {e}")
        raise HTTPException(status_code=500, detail="Failed to create testimonial")

@router.get("/", response_model=List[TestimonialResponse])
async def get_all_testimonials(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    session: AsyncSession = Depends(get_session)
):
    """Get all testimonials"""
    try:
        query = select(TestimonialSQL).order_by(desc(TestimonialSQL.created_at))
        
        if active_only:
            query = query.where(TestimonialSQL.is_active == True)
            
        query = query.offset(skip).limit(limit)
        
        result = await session.execute(query)
        testimonials = result.scalars().all()
        
        # Convert to response format
        response_data = []
        for testimonial in testimonials:
            response_data.append(TestimonialResponse(
                id=str(testimonial.id),
                name=testimonial.name,
                name_en=testimonial.name_en,
                position=testimonial.position,
                position_en=testimonial.position_en,
                text_ka=testimonial.text_ka,
                text_en=testimonial.text_en,
                rating=testimonial.rating,
                image=testimonial.image,
                is_active=testimonial.is_active,
                created_at=testimonial.created_at
            ))
        
        return response_data
        
    except Exception as e:
        logging.error(f"Error getting testimonials: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve testimonials")

@router.get("/all", response_model=List[TestimonialResponse])
async def get_all_testimonials_admin(
    session: AsyncSession = Depends(get_session)
):
    """Get all testimonials for admin panel (including inactive)"""
    try:
        query = select(TestimonialSQL).order_by(desc(TestimonialSQL.created_at))
        
        result = await session.execute(query)
        testimonials = result.scalars().all()
        
        # Convert to response format
        response_data = []
        for testimonial in testimonials:
            response_data.append(TestimonialResponse(
                id=str(testimonial.id),
                name=testimonial.name,
                name_en=testimonial.name_en,
                position=testimonial.position,
                position_en=testimonial.position_en,
                text_ka=testimonial.text_ka,
                text_en=testimonial.text_en,
                rating=testimonial.rating,
                image=testimonial.image,
                is_active=testimonial.is_active,
                created_at=testimonial.created_at
            ))
        
        return response_data
        
    except Exception as e:
        logging.error(f"Error getting all testimonials for admin: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve testimonials")

@router.get("/{testimonial_id}", response_model=TestimonialResponse)
async def get_testimonial(
    testimonial_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get testimonial by ID"""
    try:
        query = select(TestimonialSQL).where(TestimonialSQL.id == testimonial_id)
        result = await session.execute(query)
        testimonial = result.scalar_one_or_none()
        
        if not testimonial:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        return TestimonialResponse(
            id=str(testimonial.id),
            name=testimonial.name,
            name_en=testimonial.name_en,
            position=testimonial.position,
            position_en=testimonial.position_en,
            text_ka=testimonial.text_ka,
            text_en=testimonial.text_en,
            rating=testimonial.rating,
            image=testimonial.image,
            is_active=testimonial.is_active,
            created_at=testimonial.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting testimonial {testimonial_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve testimonial")

@router.put("/{testimonial_id}", response_model=dict)
async def update_testimonial(
    testimonial_id: str,
    testimonial_update: TestimonialUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update testimonial"""
    try:
        # Check if testimonial exists
        query = select(TestimonialSQL).where(TestimonialSQL.id == testimonial_id)
        result = await session.execute(query)
        existing_testimonial = result.scalar_one_or_none()
        
        if not existing_testimonial:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        # Update fields
        update_data = testimonial_update.dict(exclude_unset=True)
        if update_data:
            stmt = update(TestimonialSQL).where(
                TestimonialSQL.id == testimonial_id
            ).values(**update_data)
            
            await session.execute(stmt)
            await session.commit()
        
        return {"success": True, "message": "Testimonial updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        logging.error(f"Error updating testimonial {testimonial_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update testimonial")

@router.delete("/{testimonial_id}", response_model=dict)
async def delete_testimonial(
    testimonial_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Delete testimonial"""
    try:
        # Check if testimonial exists
        query = select(TestimonialSQL).where(TestimonialSQL.id == testimonial_id)
        result = await session.execute(query)
        existing_testimonial = result.scalar_one_or_none()
        
        if not existing_testimonial:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        # Delete testimonial
        stmt = delete(TestimonialSQL).where(TestimonialSQL.id == testimonial_id)
        await session.execute(stmt)
        await session.commit()
        
        return {"success": True, "message": "Testimonial deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        logging.error(f"Error deleting testimonial {testimonial_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete testimonial")