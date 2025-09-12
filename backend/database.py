"""
PostgreSQL Database Connection and Session Management
DataLab Georgia - Migration from MongoDB to PostgreSQL
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection settings
POSTGRES_URL = os.environ.get(
    'POSTGRES_URL', 
    'postgresql+asyncpg://datalab_user:datalab_pass123@localhost:5432/datalab_georgia'
)

# Create async engine
engine = create_async_engine(
    POSTGRES_URL,
    echo=True,  # Set to False in production
    future=True
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base class for ORM models
Base = declarative_base()

async def get_session():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    """Close database connections"""
    await engine.dispose()