from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from schemas.patient import Patient, CreatePatient, UpdatePatient
from repositories.patients import (
    get_patient,
    create_patient,
    update_patient,
    delete_patient,
    list_patients,
)


router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


# ============================================================
# List patients
# ============================================================

@router.get(
    "",
    response_model=list[Patient],
)
def list_patients_endpoint():
    return list_patients()


# ============================================================
# Get patient
# ============================================================

@router.get(
    "/{patient_id}",
    response_model=Patient,
)
def get_patient_endpoint(patient_id: str):
    patient = get_patient(patient_id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    return patient


# ============================================================
# Create patient
# ============================================================

@router.post(
    "",
    response_model=Patient,
    status_code=status.HTTP_201_CREATED,
)
def create_patient_endpoint(
    patient: CreatePatient,
):
    try:
        created_patient = create_patient(
            first_name=patient.first_name,
            last_name=patient.last_name,
            rut=patient.rut,
            birth_date=patient.birth_date,
            sex=patient.sex,
            email=patient.email,
            phone=patient.phone,
            current_height=patient.current_height,
            current_weight=patient.current_weight,
            lives_alone=patient.lives_alone,
            bmi=patient.bmi,
            context=patient.context,
            psychological_profile=patient.psychological_profile,
        )

    except IntegrityError as e:
        if "rut" in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A patient with this RUT already exists",
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create patient",
        )

    return Patient(
        id=created_patient.id,
        first_name=created_patient.first_name,
        last_name=created_patient.last_name,
        rut=created_patient.rut,
        birth_date=created_patient.birth_date,
        sex=created_patient.sex,
        email=created_patient.email,
        phone=created_patient.phone,
        current_height=created_patient.current_height,
        current_weight=created_patient.current_weight,
        lives_alone=created_patient.lives_alone,
        bmi=created_patient.bmi,
        context=created_patient.context,
        psychological_profile=created_patient.psychological_profile,
    )


# ============================================================
# Update patient
# ============================================================

@router.put(
    "/{patient_id}",
    response_model=Patient,
)
def update_patient_endpoint(
    patient_id: str,
    patient: UpdatePatient,
):
    try:
        updated_patient = update_patient(
            patient_id=patient_id,
            first_name=patient.first_name,
            last_name=patient.last_name,
            rut=patient.rut,
            birth_date=patient.birth_date,
            sex=patient.sex,
            email=patient.email,
            phone=patient.phone,
            current_height=patient.current_height,
            current_weight=patient.current_weight,
            lives_alone=patient.lives_alone,
            bmi=patient.bmi,
            context=patient.context,
            psychological_profile=patient.psychological_profile,
        )

    except IntegrityError as e:
        if "rut" in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A patient with this RUT already exists",
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update patient",
        )

    if updated_patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    return Patient(
        id=updated_patient.id,
        first_name=updated_patient.first_name,
        last_name=updated_patient.last_name,
        rut=updated_patient.rut,
        birth_date=updated_patient.birth_date,
        sex=updated_patient.sex,
        email=updated_patient.email,
        phone=updated_patient.phone,
        current_height=updated_patient.current_height,
        current_weight=updated_patient.current_weight,
        lives_alone=updated_patient.lives_alone,
        bmi=updated_patient.bmi,
        context=updated_patient.context,
        psychological_profile=updated_patient.psychological_profile,
    )


# ============================================================
# Delete patient
# ============================================================

@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_patient_endpoint(patient_id: str):
    deleted = delete_patient(patient_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    return None