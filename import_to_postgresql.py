#!/usr/bin/env python3
"""
PostgreSQL Data Import Script for DataLab Georgia
Imports data from exported MongoDB JSON files to PostgreSQL
"""

import os
import json
import asyncio
import asyncpg
from datetime import datetime
from decimal import Decimal

# PostgreSQL connection settings
PG_HOST = 'localhost'
PG_PORT = 5432
PG_DATABASE = 'datalab_georgia'
PG_USER = 'datalab_user'
PG_PASSWORD = 'datalab_pass123'

async def import_postgresql_data():
    """Import all data to PostgreSQL"""
    print(f"🔄 Connecting to PostgreSQL: {PG_HOST}:{PG_PORT}/{PG_DATABASE}")
    
    try:
        # Connect to PostgreSQL
        conn = await asyncpg.connect(
            host=PG_HOST,
            port=PG_PORT,
            database=PG_DATABASE,
            user=PG_USER,
            password=PG_PASSWORD
        )
        
        print("✅ Connected to PostgreSQL successfully")
        
        # Import Service Requests
        print("📥 Importing service_requests...")
        try:
            with open('/app/service_requests.json', 'r', encoding='utf-8') as f:
                service_requests = json.load(f)
            
            imported_count = 0
            for sr in service_requests:
                try:
                    # Parse dates
                    created_at = datetime.fromisoformat(sr['created_at'].replace('Z', '+00:00')) if sr.get('created_at') else None
                    started_at = datetime.fromisoformat(sr['started_at'].replace('Z', '+00:00')) if sr.get('started_at') else None
                    completed_at = datetime.fromisoformat(sr['completed_at'].replace('Z', '+00:00')) if sr.get('completed_at') else None
                    estimated_completion = datetime.fromisoformat(sr['estimated_completion'].replace('Z', '+00:00')) if sr.get('estimated_completion') else None
                    
                    await conn.execute("""
                        INSERT INTO service_requests 
                        (id, name, email, phone, device_type, problem_description, urgency, status, case_id,
                         created_at, started_at, completed_at, estimated_completion, price, is_read, is_archived, approved_for_kanban, admin_comment)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
                    """, 
                        sr.get('id'),
                        sr.get('name'),
                        sr.get('email'),
                        sr.get('phone'),
                        sr.get('device_type'),
                        sr.get('problem_description'),
                        sr.get('urgency'),
                        sr.get('status', 'pending'),
                        sr.get('case_id'),
                        created_at,
                        started_at,
                        completed_at,
                        estimated_completion,
                        Decimal(str(sr['price'])) if sr.get('price') else None,
                        sr.get('is_read', False),
                        sr.get('is_archived', False),
                        sr.get('approved_for_kanban', False),
                        sr.get('admin_comment')
                    )
                    imported_count += 1
                except Exception as e:
                    print(f"⚠️  Error importing service request {sr.get('case_id', 'unknown')}: {e}")
            
            print(f"✅ Imported {imported_count} service requests")
        
        except FileNotFoundError:
            print("⚠️  service_requests.json not found, skipping...")
        except Exception as e:
            print(f"❌ Error importing service requests: {e}")
        
        # Import Contact Messages
        print("📥 Importing contact_messages...")
        try:
            with open('/app/contact_messages.json', 'r', encoding='utf-8') as f:
                contact_messages = json.load(f)
            
            imported_count = 0
            for cm in contact_messages:
                try:
                    created_at = datetime.fromisoformat(cm['created_at'].replace('Z', '+00:00')) if cm.get('created_at') else None
                    
                    await conn.execute("""
                        INSERT INTO contact_messages 
                        (id, name, email, phone, subject, message, created_at, status)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    """,
                        cm.get('id'),
                        cm.get('name'),
                        cm.get('email'),
                        cm.get('phone'),
                        cm.get('subject'),
                        cm.get('message'),
                        created_at,
                        cm.get('status', 'new')
                    )
                    imported_count += 1
                except Exception as e:
                    print(f"⚠️  Error importing contact message: {e}")
            
            print(f"✅ Imported {imported_count} contact messages")
        
        except FileNotFoundError:
            print("⚠️  contact_messages.json not found, skipping...")
        except Exception as e:
            print(f"❌ Error importing contact messages: {e}")
        
        # Import Testimonials
        print("📥 Importing testimonials...")
        try:
            with open('/app/testimonials.json', 'r', encoding='utf-8') as f:
                testimonials = json.load(f)
            
            imported_count = 0
            for t in testimonials:
                try:
                    created_at = datetime.fromisoformat(t['created_at'].replace('Z', '+00:00')) if t.get('created_at') else None
                    
                    await conn.execute("""
                        INSERT INTO testimonials 
                        (id, name, name_en, position, position_en, text_ka, text_en, rating, image, is_active, created_at)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                    """,
                        t.get('id'),
                        t.get('name'),
                        t.get('name_en'),
                        t.get('position'),
                        t.get('position_en'),
                        t.get('text_ka'),
                        t.get('text_en'),
                        t.get('rating', 5),
                        t.get('image'),
                        t.get('is_active', True),
                        created_at
                    )
                    imported_count += 1
                except Exception as e:
                    print(f"⚠️  Error importing testimonial: {e}")
            
            print(f"✅ Imported {imported_count} testimonials")
        
        except FileNotFoundError:
            print("⚠️  testimonials.json not found, skipping...")
        except Exception as e:
            print(f"❌ Error importing testimonials: {e}")
        
        # Verify imports
        print("\n📊 Verification:")
        
        service_count = await conn.fetchval("SELECT COUNT(*) FROM service_requests")
        contact_count = await conn.fetchval("SELECT COUNT(*) FROM contact_messages")
        testimonial_count = await conn.fetchval("SELECT COUNT(*) FROM testimonials")
        
        print(f"  - Service Requests: {service_count}")
        print(f"  - Contact Messages: {contact_count}")
        print(f"  - Testimonials: {testimonial_count}")
        
        # Update sequence for case_id generation
        max_case_num = await conn.fetchval("""
            SELECT COALESCE(MAX(CAST(SUBSTRING(case_id FROM 7) AS INTEGER)), 0) 
            FROM service_requests 
            WHERE case_id ~ '^DL[0-9]{4}[0-9]{3}$'
        """)
        
        if max_case_num:
            await conn.execute(f"SELECT setval('case_id_seq', {max_case_num + 1})")
            print(f"  - Case ID sequence updated to: {max_case_num + 1}")
        
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection error: {e}")
        return False
    
    finally:
        try:
            await conn.close()
        except:
            pass

if __name__ == "__main__":
    result = asyncio.run(import_postgresql_data())
    
    if result:
        print("\n🎉 PostgreSQL data import completed successfully!")
    else:
        print("\n💥 PostgreSQL data import failed!")