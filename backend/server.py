"""
DataLab Georgia FastAPI Server
Migrated from MongoDB to PostgreSQL
"""

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime

# PostgreSQL imports
from database import get_session, init_db, close_db
from sqlalchemy.ext.asyncio import AsyncSession

# Import PostgreSQL route modules
from routes.service_requests_pg import router as service_requests_router
from routes.contact_pg import router as contact_router
from routes.price_estimate_pg import router as price_estimate_router
from routes.testimonials_pg import router as testimonials_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(
    title="DataLab Georgia API",
    description="Data Recovery Service API - PostgreSQL Version",
    version="2.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Health check endpoints
@api_router.get("/")
async def root():
    return {"message": "DataLab Georgia API is running", "status": "healthy", "database": "PostgreSQL"}

@api_router.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    """Health check with database connectivity verification"""
    try:
        # Test database connection
        from sqlalchemy.sql import text
        result = await session.execute(text("SELECT 1"))
        db_status = "connected" if result else "disconnected"
        
        return {
            "status": "healthy",
            "database": db_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@api_router.post("/status-check")
async def create_status_check(status_check: StatusCheckCreate):
    """Simple status check endpoint for monitoring"""
    return {
        "id": str(uuid.uuid4()),
        "client_name": status_check.client_name,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "received"
    }

# Include all route modules
api_router.include_router(service_requests_router, prefix="/service-requests", tags=["service-requests"])
api_router.include_router(contact_router, prefix="/contact", tags=["contact"])
api_router.include_router(price_estimate_router, prefix="/price-estimate", tags=["price-estimate"])
api_router.include_router(testimonials_router, prefix="/testimonials", tags=["testimonials"])

# Include API router in main app
app.include_router(api_router)

# Static file serving (frontend)
static_dir = Path(__file__).parent.parent / "frontend" / "build"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir / "static")), name="static")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve React frontend for all non-API routes"""
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        file_path = static_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        else:
            # Return index.html for SPA routing
            return FileResponse(static_dir / "index.html")

# Application lifecycle events
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    try:
        await init_db()
        logging.info("✅ PostgreSQL database initialized successfully")
    except Exception as e:
        logging.error(f"❌ Database initialization failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    try:
        await close_db()
        logging.info("✅ Database connections closed successfully")
    except Exception as e:
        logging.error(f"❌ Error closing database connections: {e}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        access_log=True
    )