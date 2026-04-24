from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.predict import router as predict_router
from app.services.model_service import get_model_status

app = FastAPI(title="Bushfire Detection API")

BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_UPLOAD_DIR = BASE_DIR / "temp_uploads"
STATIC_DIR = BASE_DIR / "static"

TEMP_UPLOAD_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health_check():
    return {"message": "Backend is running"}

@app.get("/model-status")
def model_status():
    return get_model_status()

app.include_router(predict_router)
