import uuid
from sqlalchemy import select
from database.connection import SessionLocal
from models.health_center import HealthCenter


def get_health_center(health_center_id: str):
    db = SessionLocal()
    try:
        return db.execute(select(HealthCenter).where(HealthCenter.id == health_center_id)).scalar_one_or_none()
    finally:
        db.close()


def list_health_centers():
    db = SessionLocal()
    try:
        return list(db.execute(select(HealthCenter)).scalars().all())
    finally:
        db.close()


def create_health_center(name: str, city: str, address: str = None, phone: str = None, email: str = None):
    db = SessionLocal()
    try:
        center = HealthCenter(
            id=str(uuid.uuid4()),
            name=name,
            city=city,
            address=address,
            phone=phone,
            email=email,
        )
        db.add(center)
        db.commit()
        db.refresh(center)
        return center
    finally:
        db.close()


def update_health_center(health_center_id: str, **fields):
    db = SessionLocal()
    try:
        center = db.execute(select(HealthCenter).where(HealthCenter.id == health_center_id)).scalar_one_or_none()
        if center is None:
            return None
        for field, value in fields.items():
            if hasattr(center, field) and value is not None:
                setattr(center, field, value)
        db.commit()
        db.refresh(center)
        return center
    finally:
        db.close()


def delete_health_center(health_center_id: str):
    db = SessionLocal()
    try:
        center = db.execute(select(HealthCenter).where(HealthCenter.id == health_center_id)).scalar_one_or_none()
        if center is None:
            return None
        db.delete(center)
        db.commit()
        return center
    finally:
        db.close()