from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI(title="Auth Service", version="1.0.0")

class HealthCheck(BaseModel):
    status: str = "ok"

@app.get("/healthz", response_model=HealthCheck, status_code=status.HTTP_200_OK)
def healthz():
    """
    Liveness probe.
    """
    return HealthCheck(status="ok")

@app.get("/readyz", response_model=HealthCheck, status_code=status.HTTP_200_OK)
def readyz():
    """
    Readiness probe.
    TODO: Check DB connection
    """
    return HealthCheck(status="ok")

@app.get("/")
def root():
    return {"service": "auth-service", "version": "1.0.0"}

# Mock Login for MVP
from schemas import Token, UserCreate

@app.post("/auth/login", response_model=Token)
def login(user_data: UserCreate):
    # In real world: verify password
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}
