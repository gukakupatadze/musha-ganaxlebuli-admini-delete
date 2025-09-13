"""
Seed PostgreSQL Database with Sample Data
DataLab Georgia - PostgreSQL Version
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from models.TestimonialSQL import TestimonialSQL
from models.ServiceRequestSQL import ServiceRequestSQL
from datetime import datetime, timedelta

async def seed_testimonials():
    """Seed testimonials data"""
    async with AsyncSessionLocal() as session:
        try:
            # Check if testimonials already exist
            from sqlalchemy import select, func
            count = await session.scalar(select(func.count(TestimonialSQL.id)))
            
            if count > 0:
                print(f"ℹ️  Testimonials already exist ({count} records)")
                return
            
            testimonials_data = [
                TestimonialSQL(
                    name="ნინო ღაღანიძე",
                    name_en="Nino Ghaganidze",
                    position="ბიზნეს ანალიტიკოსი",
                    position_en="Business Analyst",
                    text_ka="DataLab Georgia-მ ჩემი კომპანიის მნიშვნელოვანი მონაცემები აღადგინა დაზიანებული SSD-დან. შედეგი შესანიშნავი იყო!",
                    text_en="DataLab Georgia recovered my company's important data from a damaged SSD. The result was excellent!",
                    rating=5,
                    image="https://images.unsplash.com/photo-1494790108755-2616b612b754?w=150&h=150&fit=crop&crop=face"
                ),
                TestimonialSQL(
                    name="გიორგი კვარაცხელია",
                    name_en="Giorgi Kvaratskhelia",
                    position="IT მენეჯერი",
                    position_en="IT Manager",
                    text_ka="პროფესიონალური მიდგომა და სწრაფი მომსახურება. RAID მასივიდან 100% მონაცემები აღადგინეს.",
                    text_en="Professional approach and fast service. They recovered 100% of data from our RAID array.",
                    rating=5,
                    image="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face"
                ),
                TestimonialSQL(
                    name="ელენე მამუკელაშვილი",
                    name_en="Elene Mamukelashvili",
                    position="ფოტოგრაფი",
                    position_en="Photographer",
                    text_ka="დაზიანებული SD ბარათიდან ყველა ფოტო აღადგინეს. ძალიან კმაყოფილი ვარ სერვისით!",
                    text_en="They recovered all photos from my damaged SD card. Very satisfied with the service!",
                    rating=5,
                    image="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face"
                )
            ]
            
            for testimonial in testimonials_data:
                session.add(testimonial)
            
            await session.commit()
            print(f"✅ Inserted {len(testimonials_data)} testimonials")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding testimonials: {e}")

async def seed_sample_requests():
    """Seed sample service requests"""
    async with AsyncSessionLocal() as session:
        try:
            # Check if requests already exist
            from sqlalchemy import select, func
            count = await session.scalar(select(func.count(ServiceRequestSQL.id)))
            
            if count > 0:
                print(f"ℹ️  Service requests already exist ({count} records)")
                return
            
            # Create sample requests
            sample_requests = [
                ServiceRequestSQL(
                    case_id="DL2025001",
                    name="ნინო თბილელი",
                    email="nino@example.com",
                    phone="+995555123456",
                    device_type="hdd",
                    problem_description="ლეპტოპის მყარი დისკი აღარ მუშაობს. მნიშვნელოვანი სამუშაო ფაილები იყო შენახული.",
                    urgency="high",
                    status="pending",
                    estimated_completion=datetime.utcnow() + timedelta(days=2)
                ),
                ServiceRequestSQL(
                    case_id="DL2025002",
                    name="გიორგი ბათუმელი",
                    email="giorgi@example.com",
                    phone="+995555654321",
                    device_type="ssd",
                    problem_description="SSD დისკი დაზიანდა და ფაილები არ იკითხება. ფოტოები და დოკუმენტები უნდა აღვადგინო.",
                    urgency="medium",
                    status="in_progress",
                    started_at=datetime.utcnow() - timedelta(days=1),
                    estimated_completion=datetime.utcnow() + timedelta(days=3)
                )
            ]
            
            for request in sample_requests:
                session.add(request)
            
            await session.commit()
            print(f"✅ Inserted {len(sample_requests)} sample service requests")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding service requests: {e}")

async def main():
    """Run all seed operations"""
    print("🌱 Seeding PostgreSQL database...")
    await seed_testimonials()
    await seed_sample_requests()
    print("✅ Database seeding completed!")

if __name__ == "__main__":
    asyncio.run(main())