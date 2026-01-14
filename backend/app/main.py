from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.templates import router as template_router
from app.api.generate import router as generate_router

app = FastAPI(title="Visiting Card API")

# ✅ ADD THIS BLOCK (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://poster-web-black.vercel.app",
        "http://localhost:5173",   # React (Vite)
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(template_router, prefix="/templates")
app.include_router(generate_router, prefix="/generate")

@app.get("/")
def root():
    return {"status": "Visiting Card API running"}
