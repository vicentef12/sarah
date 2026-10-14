from datetime import date
from pydantic import BaseModel


class Patient(BaseModel):
    id: str
    first_name: str
    last_name: str
    rut: str
    birth_date: date
    sex: str
    email: str
    phone: str
    current_height: float
    current_weight: float
    lives_alone: bool
    bmi: float
    context: str
    psychological_profile: str


class CreatePatient(BaseModel):
    first_name: str
    last_name: str
    rut: str
    birth_date: date
    sex: str
    email: str
    phone: str
    current_height: float
    current_weight: float
    lives_alone: bool
    bmi: float
    context: str
    psychological_profile: str


class UpdatePatient(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    rut: str | None = None
    birth_date: date | None = None
    sex: str | None = None
    email: str | None = None
    phone: str | None = None
    current_height: float | None = None
    current_weight: float | None = None
    lives_alone: bool | None = None
    bmi: float | None = None
    context: str | None = None
    psychological_profile: str | None = None