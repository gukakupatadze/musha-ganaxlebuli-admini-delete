#!/usr/bin/env python3
"""
MongoDB Data Export Script for DataLab Georgia
Exports data from MongoDB collections to JSON files for PostgreSQL migration
"""

import os
import json
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'datalab_georgia')

async def export_mongodb_data():
    """Export all data from MongoDB collections"""
    print(f"🔄 Connecting to MongoDB: {MONGO_URL}")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB successfully")
        
        # Collections to export
        collections = {
            'service_requests': 'service_requests.json',
            'contact_messages': 'contact_messages.json', 
            'testimonials': 'testimonials.json',
            'status_checks': 'status_checks.json'  # Optional - for health checks
        }
        
        exported_data = {}
        
        for collection_name, filename in collections.items():
            print(f"📤 Exporting {collection_name}...")
            
            try:
                # Get all documents from collection
                cursor = db[collection_name].find({})
                documents = await cursor.to_list(None)  # Get all documents
                
                # Convert ObjectId to string for JSON serialization
                for doc in documents:
                    if '_id' in doc:
                        doc['_id'] = str(doc['_id'])
                    
                    # Convert datetime objects to ISO format
                    for key, value in doc.items():
                        if isinstance(value, datetime):
                            doc[key] = value.isoformat()
                
                exported_data[collection_name] = documents
                print(f"✅ Exported {len(documents)} documents from {collection_name}")
                
                # Save to individual JSON files
                with open(f'/app/{filename}', 'w', encoding='utf-8') as f:
                    json.dump(documents, f, ensure_ascii=False, indent=2)
                
            except Exception as e:
                print(f"❌ Error exporting {collection_name}: {e}")
                exported_data[collection_name] = []
        
        # Save combined export
        with open('/app/mongodb_export_all.json', 'w', encoding='utf-8') as f:
            json.dump(exported_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 Export Summary:")
        for collection_name, data in exported_data.items():
            print(f"  - {collection_name}: {len(data)} records")
        
        print(f"\n💾 Exported files saved to:")
        print(f"  - /app/mongodb_export_all.json (combined)")
        for filename in collections.values():
            print(f"  - /app/{filename}")
            
        return exported_data
        
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        return {}
    
    finally:
        client.close()

if __name__ == "__main__":
    result = asyncio.run(export_mongodb_data())
    
    if result:
        print("\n🎉 MongoDB data export completed successfully!")
    else:
        print("\n💥 MongoDB data export failed!")