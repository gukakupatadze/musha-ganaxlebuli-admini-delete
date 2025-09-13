"""
Initialize PostgreSQL Database for DataLab Georgia
Creates database, user, and required sequences
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def init_database():
    """Initialize PostgreSQL database and user"""
    try:
        # Connect to default postgres database to create our database
        conn = await asyncpg.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='postgres',
            database='postgres'
        )
        
        # Create database if it doesn't exist
        try:
            await conn.execute('CREATE DATABASE datalab_georgia')
            print("✅ Database 'datalab_georgia' created")
        except asyncpg.DuplicateDatabaseError:
            print("ℹ️  Database 'datalab_georgia' already exists")
        except Exception as e:
            if "already exists" in str(e):
                print("ℹ️  Database 'datalab_georgia' already exists")
            else:
                print(f"Database creation error: {e}")
        
        # Create user if it doesn't exist
        try:
            await conn.execute("""
                CREATE USER datalab_user WITH PASSWORD 'datalab_pass123'
            """)
            print("✅ User 'datalab_user' created")
        except asyncpg.DuplicateObjectError:
            print("ℹ️  User 'datalab_user' already exists")
        except Exception as e:
            if "already exists" in str(e):
                print("ℹ️  User 'datalab_user' already exists")
            else:
                print(f"User creation error: {e}")
        
        # Grant privileges
        try:
            await conn.execute('GRANT ALL PRIVILEGES ON DATABASE datalab_georgia TO datalab_user')
            print("✅ Privileges granted to datalab_user")
        except Exception as e:
            print(f"Privilege grant error: {e}")
        
        await conn.close()
        
        # Connect to our database to create sequences
        conn = await asyncpg.connect(
            host='localhost',
            port=5432,
            user='datalab_user',
            password='datalab_pass123',
            database='datalab_georgia'
        )
        
        # Create case_id_seq sequence
        try:
            await conn.execute('CREATE SEQUENCE IF NOT EXISTS case_id_seq START 1')
            print("✅ Sequence 'case_id_seq' created")
        except Exception as e:
            print(f"Sequence creation error: {e}")
        
        await conn.close()
        print("🎉 Database initialization completed!")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")

if __name__ == "__main__":
    asyncio.run(init_database())