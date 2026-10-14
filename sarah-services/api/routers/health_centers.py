from fastapi import APIRouter, HTTPException, status
from repositories import health_centers as repo
from schemas.health_center import (
    HealthCenterCreate,
    HealthCenterResponse,
    HealthCenterUpdate,
)

router = APIRouter(prefix="/health-centers", tags=["Health Centers"])


@router.post("/", response_model=HealthCenterResponse, status_code=status.HTTP_201_CREATED)
def create_health_center(data: HealthCenterCreate):
    try:
        return repo.create_health_center(
            name=data.name,
            city=data.city,
            address=data.address,
            phone=data.phone,
            email=data.email,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en BD/Repo: {str(e)}"
        )


@router.get("/", response_model=list[HealthCenterResponse])
def list_health_centers():
    return repo.list_health_centers()


@router.get("/{center_id}", response_model=HealthCenterResponse)
def get_health_center(center_id: str):
    center = repo.get_health_center(center_id)
    if not center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de salud con id '{center_id}' no encontrado",
        )
    return center


@router.put("/{center_id}", response_model=HealthCenterResponse)
def update_health_center(center_id: str, data: HealthCenterUpdate):
    center = repo.update_health_center(center_id, **data.model_dump(exclude_unset=True))
    if not center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de salud con id '{center_id}' no encontrado",
        )
    return center


@router.delete("/{center_id}", response_model=HealthCenterResponse)
def delete_health_center(center_id: str):
    center = repo.delete_health_center(center_id)
    if not center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de salud con id '{center_id}' no encontrado",
        )
    return center