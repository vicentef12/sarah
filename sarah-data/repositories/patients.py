import uuid

from datetime import date

from sqlalchemy import select

from database.connection import SessionLocal
from models.patient import Patient


def get_patient(
    patient_id: str,
):
    db = SessionLocal()

    try:

        statement = select(Patient).where(
            Patient.id == patient_id
        )

        return db.execute(
            statement
        ).scalar_one_or_none()

    finally:

        db.close()


def create_patient(
    first_name: str,
    last_name: str,
    rut: str,
    birth_date: date,
    sex: str,
    email: str,
    phone: str,
    current_height: float,
    current_weight: float,
    lives_alone: bool,
    bmi: float,
    context: str,
    psychological_profile: str,
):
    db = SessionLocal()

    try:

        patient = Patient(
            id=str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            rut=rut,
            birth_date=birth_date,
            sex=sex,
            email=email,
            phone=phone,
            current_height=current_height,
            current_weight=current_weight,
            lives_alone=lives_alone,
            bmi=bmi,
            context=context,
            psychological_profile=psychological_profile,
        )

        db.add(patient)

        db.commit()

        db.refresh(patient)

        return patient

    finally:

        db.close()


def update_patient(
    patient_id: str,
    **fields,
):
    db = SessionLocal()

    try:

        statement = select(Patient).where(
            Patient.id == patient_id
        )

        patient = db.execute(
            statement
        ).scalar_one_or_none()

        if patient is None:

            return None

        for field, value in fields.items():

            if hasattr(patient, field):

                setattr(
                    patient,
                    field,
                    value,
                )

        db.commit()

        db.refresh(patient)

        return patient

    finally:

        db.close()


def delete_patient(
    patient_id: str,
):
    db = SessionLocal()

    try:

        statement = select(Patient).where(
            Patient.id == patient_id
        )

        patient = db.execute(
            statement
        ).scalar_one_or_none()

        if patient is None:

            return None

        db.delete(patient)

        db.commit()

        return patient

    finally:

        db.close()


def list_patients():
    db = SessionLocal()
    try:
        return list(db.execute(select(Patient)).scalars().all())
    finally:
        db.close()