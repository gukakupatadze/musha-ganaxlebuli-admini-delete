"""
Create all database tables for DataLab Georgia
PostgreSQL version with proper constraints and indexes
"""

import asyncio
from database import engine, Base
from models.ContactMessageSQL import ContactMessageSQL
from models.ServiceRequestSQL import ServiceRequestSQL
from models.TestimonialSQL import TestimonialSQL

async def create_tables():
    """Create all database tables"""
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            print("✅ All database tables created successfully!")
            
            # Create indexes for better performance
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_service_requests_case_id 
                ON service_requests(case_id);
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_service_requests_status 
                ON service_requests(status);
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_service_requests_created_at 
                ON service_requests(created_at);
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_contact_messages_status 
                ON contact_messages(status);
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_contact_messages_created_at 
                ON contact_messages(created_at);
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_testimonials_active 
                ON testimonials(is_active);
            """)
            
            print("✅ Database indexes created successfully!")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    asyncio.run(create_tables())