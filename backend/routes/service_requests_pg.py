"""
Service Requests API Routes - PostgreSQL Version
DataLab Georgia - Migration from MongoDB to PostgreSQL
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, desc, func
from sqlalchemy.sql import text
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from database import get_session
from models.ServiceRequestSQL import (
    ServiceRequestSQL, 
    ServiceRequestCreate, 
    ServiceRequestUpdate, 
    ServiceRequestResponse
)

router = APIRouter()

@router.post("/", response_model=dict)
async def create_service_request(
    request: ServiceRequestCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new service request"""
    try:
        # Generate case ID using database sequence
        case_id_result = await session.execute(
            text("SELECT 'DL' || EXTRACT(YEAR FROM NOW()) || LPAD(nextval('case_id_seq')::text, 3, '0')")
        )
        case_id = case_id_result.scalar()
        
        # Calculate estimated completion (3 days from now)
        estimated_completion = datetime.utcnow() + timedelta(days=3)
        
        # Create new service request
        new_request = ServiceRequestSQL(
            case_id=case_id,
            name=request.name,
            email=request.email,
            phone=request.phone,
            device_type=request.device_type,
            problem_description=request.problem_description,
            urgency=request.urgency,
            estimated_completion=estimated_completion
        )
        
        session.add(new_request)
        await session.commit()
        await session.refresh(new_request)
        
        return {
            "success": True,
            "message": "Service request created successfully",
            "case_id": case_id,
            "estimated_completion": estimated_completion.isoformat()
        }
        
    except Exception as e:
        await session.rollback()
        logging.error(f"Error creating service request: {e}")
        raise HTTPException(status_code=500, detail="Failed to create service request")

@router.get("/", response_model=List[ServiceRequestResponse])
async def get_all_service_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session)
):
    """Get all service requests with optional filtering"""
    try:
        # Build query
        query = select(ServiceRequestSQL).order_by(desc(ServiceRequestSQL.created_at))
        
        if status:
            query = query.where(ServiceRequestSQL.status == status)
            
        query = query.offset(skip).limit(limit)
        
        result = await session.execute(query)
        requests = result.scalars().all()
        
        # Convert to response format
        response_data = []
        for req in requests:
            response_data.append(ServiceRequestResponse(
                id=str(req.id),
                name=req.name,
                email=req.email,
                phone=req.phone,
                device_type=req.device_type,
                problem_description=req.problem_description,
                urgency=req.urgency,
                status=req.status,
                case_id=req.case_id,
                created_at=req.created_at,
                started_at=req.started_at,
                completed_at=req.completed_at,
                estimated_completion=req.estimated_completion.strftime('%Y-%m-%d') if req.estimated_completion else None,
                price=float(req.price) if req.price else None,
                is_read=req.is_read,
                is_archived=req.is_archived,
                approved_for_kanban=req.approved_for_kanban,
                admin_comment=req.admin_comment
            ))
        
        return response_data
        
    except Exception as e:
        logging.error(f"Error getting service requests: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve service requests")

@router.get("/approved/kanban", response_model=List[ServiceRequestResponse])
async def get_approved_requests(
    session: AsyncSession = Depends(get_session)
):
    """Get service requests approved for kanban board"""
    try:
        query = select(ServiceRequestSQL).where(
            ServiceRequestSQL.approved_for_kanban == True
        ).order_by(desc(ServiceRequestSQL.created_at))
        
        result = await session.execute(query)
        requests = result.scalars().all()
        
        # Convert to response format
        response_data = []
        for req in requests:
            response_data.append(ServiceRequestResponse(
                id=str(req.id),
                name=req.name,
                email=req.email,
                phone=req.phone,
                device_type=req.device_type,
                problem_description=req.problem_description,
                urgency=req.urgency,
                status=req.status,
                case_id=req.case_id,
                created_at=req.created_at,
                started_at=req.started_at,
                completed_at=req.completed_at,
                estimated_completion=req.estimated_completion.strftime('%Y-%m-%d') if req.estimated_completion else None,
                price=float(req.price) if req.price else None,
                is_read=req.is_read,
                is_archived=req.is_archived,
                approved_for_kanban=req.approved_for_kanban,
                admin_comment=req.admin_comment
            ))
        
        return response_data
        
    except Exception as e:
        logging.error(f"Error getting approved requests: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve approved requests")

@router.get("/archived", response_model=List[ServiceRequestResponse])
async def get_archived_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session)
):
    """Get archived service requests"""
    try:
        query = select(ServiceRequestSQL).where(
            ServiceRequestSQL.is_archived == True
        ).order_by(desc(ServiceRequestSQL.created_at))
        
        query = query.offset(skip).limit(limit)
        
        result = await session.execute(query)
        requests = result.scalars().all()
        
        # Convert to response format
        response_data = []
        for req in requests:
            response_data.append(ServiceRequestResponse(
                id=str(req.id),
                name=req.name,
                email=req.email,
                phone=req.phone,
                device_type=req.device_type,
                problem_description=req.problem_description,
                urgency=req.urgency,
                status=req.status,
                case_id=req.case_id,
                created_at=req.created_at,
                started_at=req.started_at,
                completed_at=req.completed_at,
                estimated_completion=req.estimated_completion.strftime('%Y-%m-%d') if req.estimated_completion else None,
                price=float(req.price) if req.price else None,
                is_read=req.is_read,
                is_archived=req.is_archived,
                approved_for_kanban=req.approved_for_kanban,
                admin_comment=req.admin_comment
            ))
        
        return response_data
        
    except Exception as e:
        logging.error(f"Error getting archived requests: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve archived requests")

@router.get("/{case_id}", response_model=ServiceRequestResponse)
async def get_service_request(
    case_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get service request by case ID"""
    try:
        query = select(ServiceRequestSQL).where(ServiceRequestSQL.case_id == case_id)
        result = await session.execute(query)
        request = result.scalar_one_or_none()
        
        if not request:
            raise HTTPException(status_code=404, detail="Service request not found")
        
        return ServiceRequestResponse(
            id=str(request.id),
            name=request.name,
            email=request.email,
            phone=request.phone,
            device_type=request.device_type,
            problem_description=request.problem_description,
            urgency=request.urgency,
            status=request.status,
            case_id=request.case_id,
            created_at=request.created_at,
            started_at=request.started_at,
            completed_at=request.completed_at,
            estimated_completion=request.estimated_completion.strftime('%Y-%m-%d') if request.estimated_completion else None,
            price=float(request.price) if request.price else None,
            is_read=request.is_read,
            is_archived=request.is_archived,
            approved_for_kanban=request.approved_for_kanban,
            admin_comment=request.admin_comment
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting service request {case_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve service request")

@router.put("/{request_id}", response_model=dict)
async def update_service_request(
    request_id: str,
    request_update: ServiceRequestUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update service request by ID (UUID)"""
    try:
        # Check if request exists
        query = select(ServiceRequestSQL).where(ServiceRequestSQL.id == request_id)
        result = await session.execute(query)
        existing_request = result.scalar_one_or_none()
        
        if not existing_request:
            raise HTTPException(status_code=404, detail="Service request not found")
        
        # Update fields
        update_data = request_update.dict(exclude_unset=True)
        if update_data:
            stmt = update(ServiceRequestSQL).where(
                ServiceRequestSQL.id == request_id
            ).values(**update_data)
            
            await session.execute(stmt)
            await session.commit()
        
        return {"success": True, "message": "Service request updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        logging.error(f"Error updating service request {request_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update service request")

@router.delete("/{case_id}", response_model=dict)
async def delete_service_request(
    case_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Delete service request"""
    try:
        # Check if request exists
        query = select(ServiceRequestSQL).where(ServiceRequestSQL.case_id == case_id)
        result = await session.execute(query)
        existing_request = result.scalar_one_or_none()
        
        if not existing_request:
            raise HTTPException(status_code=404, detail="Service request not found")
        
        # Delete request
        stmt = delete(ServiceRequestSQL).where(ServiceRequestSQL.case_id == case_id)
        await session.execute(stmt)
        await session.commit()
        
        return {"success": True, "message": "Service request deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        logging.error(f"Error deleting service request {case_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete service request")