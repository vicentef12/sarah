from fastapi import FastAPI
from api.routers import patients, health_centers, professionals, conversations

app = FastAPI(
    title="Sarah Services API",
    description="API REST central del Asistente Sarah",
    version="1.0.0",
)

# Registrar routers
app.include_router(patients.router)
app.include_router(health_centers.router)
app.include_router(professionals.router)
app.include_router(conversations.router)


@app.get("/")
def root():
    return {"message": "Sarah Services API is running"}