import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.predict import router as predict_router
from app.services.model_service import get_model_status

app = FastAPI(title="Bushfire Detection API")

os.makedirs("temp_uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

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