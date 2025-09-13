"""
Contact API Routes - PostgreSQL Version
DataLab Georgia - Migration from MongoDB to PostgreSQL
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, desc
from typing import List, Optional
import logging

from database import get_session
from models.ContactMessageSQL import (
    ContactMessageSQL,
    ContactMessageCreate,
    ContactMessageUpdate,
    ContactMessageResponse
)

router = APIRouter()

@router.post("/", response_model=dict)
async def create_contact_message(
    message: ContactMessageCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new contact message"""
    try:
        new_message = ContactMessageSQL(
            name=message.name,
            email=message.email,
            phone=message.phone,
            subject=message.subject,
            message=message.message
        )
        
        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)
        
        return {
            "success": True,
            "message": "Contact message sent successfully",
            "id": new_message.id
        }
        
    except Exception as e:
        await session.rollback()
        logging.error(f"Error creating contact message: {e}")
        raise HTTPException(status_code=500, detail="Failed to send contact message")

@router.get("/", response_model=List[ContactMessageResponse])
async def get_all_contact_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session)
):
    """Get all contact messages with optional filtering"""
    try:
        query = select(ContactMessageSQL).order_by(desc(ContactMessageSQL.created_at))
        
        if status:
            query = query.where(ContactMessageSQL.status == status)
            
        query = query.offset(skip).limit(limit)
        
        result = await session.execute(query)
        messages = result.scalars().all()
        
        # Convert to response format
        response_data = []
        for msg in messages:
            response_data.append(ContactMessageResponse(
                id=msg.id,
                name=msg.name,
                email=msg.email,
                phone=msg.phone,
                subject=msg.subject,
                message=msg.message,
                created_at=msg.created_at,
                status=msg.status
            ))
        
        return response_data
        
    except Exception as e:
        logging.error(f"Error getting contact messages: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve contact messages")

@router.get("/stats", response_model=dict)
async def get_contact_stats(
    session: AsyncSession = Depends(get_session)
):
    """Get contact message statistics for admin dashboard"""
    try:
        from sqlalchemy import func
        
        # Total messages
        total_count = await session.scalar(
            select(func.count(ContactMessageSQL.id))
        )
        
        # New messages (unread)
        new_count = await session.scalar(
            select(func.count(ContactMessageSQL.id)).where(
                ContactMessageSQL.status == 'new'
            )
        )
        
        # Read messages
        read_count = await session.scalar(
            select(func.count(ContactMessageSQL.id)).where(
                ContactMessageSQL.status == 'read'
            )
        )
        
        # Replied messages
        replied_count = await session.scalar(
            select(func.count(ContactMessageSQL.id)).where(
                ContactMessageSQL.status == 'replied'
            )
        )
        
        return {
            "total": total_count or 0,
            "new": new_count or 0,
            "read": read_count or 0,
            "replied": replied_count or 0
        }
        
    except Exception as e:
        logging.error(f"Error getting contact stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve contact statistics")

@router.get("/{message_id}", response_model=ContactMessageResponse)
async def get_contact_message(
    message_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get contact message by ID"""
    try:
        query = select(ContactMessageSQL).where(ContactMessageSQL.id == message_id)
        result = await session.execute(query)
        message = result.scalar_one_or_none()
        
        if not message:
            raise HTTPException(status_code=404, detail="Contact message not found")
        
        return ContactMessageResponse(
            id=message.id,
            name=message.name,
            email=message.email,
            phone=message.phone,
            subject=message.subject,
            message=message.message,
            created_at=message.created_at,
            status=message.status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting contact message {message_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve contact message")

@router.put("/{message_id}", response_model=dict)
async def update_contact_message(
    message_id: str,
    message_update: ContactMessageUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update contact message status"""
    try:
        # Check if message exists
        query = select(ContactMessageSQL).where(ContactMessageSQL.id == message_id)
        result = await session.execute(query)
        existing_message = result.scalar_one_or_none()
        
        if not existing_message:
            raise HTTPException(status_code=404, detail="Contact message not found")
        
        # Update fields
        update_data = message_update.dict(exclude_unset=True)
        if update_data:
            stmt = update(ContactMessageSQL).where(
                ContactMessageSQL.id == message_id
            ).values(**update_data)
            
            await session.execute(stmt)
            await session.commit()
        
        return {"success": True, "message": "Contact message updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        logging.error(f"Error updating contact message {message_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update contact message")

@router.delete("/{message_id}", response_model=dict)
async def delete_contact_message(
    message_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Delete contact message"""
    try:
        # Check if message exists
        query = select(ContactMessageSQL).where(ContactMessageSQL.id == message_id)
        result = await session.execute(query)
        existing_message = result.scalar_one_or_none()
        
        if not existing_message:
            raise HTTPException(status_code=404, detail="Contact message not found")
        
        # Delete message
        stmt = delete(ContactMessageSQL).where(ContactMessageSQL.id == message_id)
        await session.execute(stmt)
        await session.commit()
        
        return {"success": True, "message": "Contact message deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        logging.error(f"Error deleting contact message {message_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete contact message")