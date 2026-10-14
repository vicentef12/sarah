import uuid
from sqlalchemy import select
from database.connection import SessionLocal
from models.professional import Professional

def get_professional(professional_id: str): # (lee uno)   busca un profesional por su id y devuelve la instancia encontrada o none
    db = SessionLocal()
    try:
        return db.execute(select(Professional).where(Professional.id == professional_id)).scalar_one_or_none()
    finally:
        db.close()

def list_professionals(): # (lee todos)   devuelve una lista con todos los profesionales
    db = SessionLocal()
    try:
        return list(db.execute(select(Professional)).scalars().all())
    finally:
        db.close()

def create_professional(
    first_name: str,
    last_name: str,
    specialty: str,
    email: str,
    phone: str,
    rut: str = None,
    birth_date = None,
    sex: str = None,
    health_center_id: str | None = None,
):
    db = SessionLocal()
    try:
        prof = Professional(
            id=str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            specialty=specialty,
            rut=rut,
            birth_date=birth_date,
            sex=sex,
            email=email,
            phone=phone,
            health_center_id=health_center_id,
        )
        db.add(prof)
        db.commit()
        db.refresh(prof)
        return prof
    finally:
        db.close()

def update_professional(professional_id: str, **fields): # (actualiza)   actualiza un profesional existente con los campos proporcionados
    db = SessionLocal()
    try:
        prof = db.execute(select(Professional).where(Professional.id == professional_id)).scalar_one_or_none()
        if prof is None:
            return None
        for field, value in fields.items():
            if hasattr(prof, field) and value is not None:
                setattr(prof, field, value)
        db.commit()
        db.refresh(prof)
        return prof
    finally:
        db.close()

def delete_professional(professional_id: str): # (elimina)   elimina un profesional existente por su id
    db = SessionLocal()
    try:
        prof = db.execute(select(Professional).where(Professional.id == professional_id)).scalar_one_or_none()
        if prof is None:
            return None
        db.delete(prof)
        db.commit()
        return prof
    finally:
        db.close()