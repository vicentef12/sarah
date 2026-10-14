from pydantic import BaseModel, ConfigDict


class HealthCenterBase(BaseModel): # (define)   define la estructura base de un centro de salud con los campos name, city, address, phone y email
    name: str
    city: str
    address: str | None = None
    phone: str | None = None
    email: str | None = None


class HealthCenterCreate(HealthCenterBase): # (define)   define la estructura para crear un centro de salud, heredando de HealthCenterBase y agregando el campo id
    pass


class HealthCenterUpdate(BaseModel): # (define)   define la estructura para actualizar un centro de salud, con todos los campos opcionales
    name: str | None = None
    city: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None


class HealthCenterResponse(HealthCenterBase):# (define)   define la estructura de respuesta de un centro de salud, heredando de HealthCenterBase y agregando el campo id
    id: str

    model_config = ConfigDict(from_attributes=True)