from fastapi import FastAPI

from backend.app.api.templates import router as template_router
from backend.app.api.generate import router as generate_router

app = FastAPI(title="Visiting Card API")

# API routes
app.include_router(template_router, prefix="/templates")
app.include_router(generate_router, prefix="/generate")


@app.get("/")
def root():
    return {"status": "Visiting Card API running"}
