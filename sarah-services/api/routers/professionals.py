from fastapi import APIRouter, HTTPException, status
from repositories import professionals as repo
from schemas.professional import (
    ProfessionalCreate,
    ProfessionalResponse,
    ProfessionalUpdate,
)

router = APIRouter(prefix="/professionals", tags=["Professionals"])

@router.post("/", response_model=ProfessionalResponse, status_code=status.HTTP_201_CREATED)
def create_professional(data: ProfessionalCreate):
    try:
        return repo.create_professional(
            first_name=data.first_name,
            last_name=data.last_name,
            specialty=data.specialty,
            email=data.email,
            phone=data.phone,
            rut=getattr(data, "rut", None),
            birth_date=getattr(data, "birth_date", None),
            sex=getattr(data, "sex", None),
            health_center_id=data.health_center_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en BD/Repo: {str(e)}"
        )


@router.get("/", response_model=list[ProfessionalResponse])# (define)   define el endpoint para listar todos los profesionales, devolviendo una lista de objetos ProfessionalResponse
def list_professionals():
    return repo.list_professionals()


@router.get("/{professional_id}", response_model=ProfessionalResponse)# (define)   define el endpoint para obtener un profesional por su id, devolviendo un objeto ProfessionalResponse o lanzando una excepción si no se encuentra
def get_professional(professional_id: str):
    prof = repo.get_professional(professional_id)
    if not prof:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profesional con id '{professional_id}' no encontrado",
        )
    return prof


@router.put("/{professional_id}", response_model=ProfessionalResponse)# (define)   define el endpoint para actualizar un profesional por su id, recibiendo un objeto ProfessionalUpdate y devolviendo un objeto ProfessionalResponse
def update_professional(professional_id: str, data: ProfessionalUpdate):
    prof = repo.update_professional(professional_id, **data.model_dump(exclude_unset=True))
    if not prof:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profesional con id '{professional_id}' no encontrado",
        )
    return prof


@router.delete("/{professional_id}", response_model=ProfessionalResponse)# (define)   define el endpoint para eliminar un profesional por su id, devolviendo un objeto ProfessionalResponse o lanzando una excepción si no se encuentra
def delete_professional(professional_id: str):
    prof = repo.delete_professional(professional_id)
    if not prof:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profesional con id '{professional_id}' no encontrado",
        )
    return prof