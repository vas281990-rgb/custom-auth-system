from fastapi import FastAPI
from app.routers import auth

app = FastAPI(
    title="Custom Auth System",
    description="Custom authentication and authorization system with RBAC",
    version="1.0.0",
)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}

app.include_router(auth.router)
