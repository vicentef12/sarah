from pydantic import BaseModel, ConfigDict, EmailStr


class ProfessionalBase(BaseModel): # (define)   define la estructura base de un profesional con los campos first_name, last_name, specialty, rut, birth_date, sex, email, phone y health_center_id
    first_name: str
    last_name: str
    specialty: str
    rut: str
    birth_date: str
    sex: str
    email: str
    phone: str
    health_center_id: str


class ProfessionalCreate(ProfessionalBase): # (define)   define la estructura para crear un profesional, heredando de ProfessionalBase y agregando el campo id
    pass


class ProfessionalUpdate(BaseModel): # (define)   define la estructura para actualizar un profesional, con todos los campos opcionales
    first_name: str | None = None
    last_name: str | None = None
    specialty: str | None = None
    rut: str | None = None
    birth_date: str | None = None
    sex: str | None = None
    email: str | None = None
    phone: str | None = None
    health_center_id: str | None = None


class ProfessionalResponse(ProfessionalBase): # (define)   define la estructura de respuesta de un profesional, heredando de ProfessionalBase y agregando el campo id
    id: str

    model_config = ConfigDict(from_attributes=True)