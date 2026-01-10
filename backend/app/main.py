from fastapi import FastAPI

from app.api.templates import router as template_router
from app.api.generate import router as generate_router

app = FastAPI(title="Visiting Card API")

app.include_router(template_router, prefix="/templates")
app.include_router(generate_router, prefix="/generate")

@app.get("/")
def root():
    return {"status": "Visiting Card API running"}
