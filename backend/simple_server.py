"""
Simple FastAPI Server for DataLab Georgia
Simplified version to work in WebContainer
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

# Create the main app
app = FastAPI(title="DataLab Georgia")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "DataLab Georgia API is running"}

@app.get("/api/")
async def root():
    return {"message": "DataLab Georgia API", "status": "running"}

# Serve static files from frontend build
static_dir = Path(__file__).parent.parent / "frontend" / "build"
print(f"Static directory: {static_dir}")
print(f"Static directory exists: {static_dir.exists()}")

if static_dir.exists():
    # Mount static files
    app.mount("/static", StaticFiles(directory=str(static_dir / "static")), name="static")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve React frontend"""
        if full_path.startswith("api/"):
            return {"error": "API endpoint not found"}
        
        # For root path, serve index.html
        if full_path == "" or full_path == "/":
            return FileResponse(static_dir / "index.html")
        
        # Check if file exists
        file_path = static_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        else:
            # Return index.html for SPA routing
            return FileResponse(static_dir / "index.html")

if __name__ == "__main__":
    import uvicorn
    print("🌟 Starting DataLab Georgia server...")
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8001,
        reload=False
    )