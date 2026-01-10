from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.templates import router as template_router
from app.api.generate import router as generate_router

app = FastAPI(title="Visiting Card API")

BASE_DIR = Path(__file__).resolve().parent

# 🔥 Serve images
app.mount(
    "/storage",
    StaticFiles(directory=BASE_DIR / "storage"),
    name="storage",
)

app.include_router(template_router, prefix="/templates")
app.include_router(generate_router, prefix="/generate")
