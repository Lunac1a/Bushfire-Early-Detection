import uuid
import json

from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Form
from pathlib import Path
import shutil
from PIL import Image
import cv2

from app.services.model_service import get_model
from app.services.video_service import precess_video

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "temp_uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

OUTPUT_DIR = BASE_DIR / "static"
OUTPUT_DIR.mkdir(exist_ok=True)


def calculate_risk(smoke_count: int, fire_count: int, max_confidence: float) -> str:
    if fire_count >= 1:
        return "high"
    if smoke_count >= 2 or max_confidence >= 0.7:
        return "medium"
    if smoke_count >= 1:
        return "low"
    return "safe"


def _media_type_from_suffix(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return "image"
    if suffix in {".mp4", ".mov", ".avi", ".mkv"}:
        return "video"
    return "unknown"


def _metadata_path_for_output(file_path: Path) -> Path:
    return file_path.with_suffix(f"{file_path.suffix}.json")


def _save_output_metadata(file_path: Path, payload: dict):
    metadata_path = _metadata_path_for_output(file_path)
    metadata_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


@router.get("/recent_history")
async def recent_history(limit: int = Query(5, ge=1, le=20)):
    files = [
        path for path in OUTPUT_DIR.iterdir()
        if path.is_file() and path.suffix.lower() != ".json"
    ]
    files.sort(key=lambda path: path.stat().st_mtime, reverse=True)

    items = []
    for path in files[:limit]:
        stat = path.stat()
        metadata = None
        metadata_path = _metadata_path_for_output(path)
        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                metadata = None

        items.append({
            "filename": path.name,
            "media_type": _media_type_from_suffix(path),
            "url": f"/static/{path.name}",
            "size_bytes": stat.st_size,
            "updated_at": stat.st_mtime,
            "result_data": metadata,
        })

    return {"items": items}

@router.post("/predict")
async def predict(
        file: UploadFile = File(...),
        model: str = Query("v8s")
):
    # Check if it's a picture
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    # Save files
    input_filename = f"{uuid.uuid4()}_{file.filename}"
    output_filename = f"{uuid.uuid4()}_result.jpg"
    file_path = UPLOAD_DIR / input_filename
    output_path = OUTPUT_DIR / output_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        with Image.open(file_path) as image:
            width, height = image.size

        yolo_model = get_model(model)
        results = yolo_model(str(file_path), conf=0.4)
        result = results[0]

        detections = []
        smoke_count = 0
        fire_count = 0
        max_confidence = 0.0

        if result.boxes is not None:
            for box in result.boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                xyxy = box.xyxy[0].tolist()
                class_name = result.names[cls_id]

                if class_name.lower() == "smoke":
                    smoke_count += 1
                elif class_name.lower() == "fire":
                    fire_count +=1

                max_confidence = max(max_confidence, conf)

                detections.append({
                    "class_name": class_name,
                    "confidence": round(conf, 4),
                    "bbox": [round(x, 2) for x in xyxy]
                })

        risk_level = calculate_risk(smoke_count, fire_count, max_confidence)
        annotated_image = result.plot()
        if not cv2.imwrite(str(output_path), annotated_image):
            raise ValueError("Failed to save output image.")
        response_payload = {
            "model_used": model,
            "filename": file.filename,
            "image_width": width,
            "image_height": height,
            "output_image_url": f"/static/{output_filename}",
            "detections": detections,
            "risk_level": risk_level,
            "summary": {
                "smoke_count": smoke_count,
                "fire_count": fire_count,
                "max_confidence": round(max_confidence, 4)
            }
        }
        _save_output_metadata(output_path, response_payload)
        return response_payload

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # delete temp files
        try:
            if file_path.exists():
                file_path.unlink()
        except PermissionError:
            print(f"Warning: could not delete temp file {file_path}")

@router.post("/predict_video")
async def predict_video(
        file: UploadFile = File(...),
        model: str = Form("v8s")
):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Unsupported video format.")

    input_filename = f"{uuid.uuid4()}_{file.filename}"
    output_filename = f"{uuid.uuid4()}_result.mp4"

    input_path = UPLOAD_DIR / input_filename
    output_path = OUTPUT_DIR / output_filename

    try:
        with input_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        yolo_model = get_model(model)

        if isinstance(yolo_model, list):
            yolo_model = yolo_model[0]

        stats = precess_video(
            input_path=str(input_path),
            output_path=str(output_path),
            model=yolo_model,
            frame_skip=5
        )

        risk_level = calculate_risk(
            smoke_count=stats["smoke_frames"],
            fire_count=stats["fire_frames"],
            max_confidence=stats["max_confidence"],
        )
        response_payload = {
            "message": "Video processed successfully.",
            "model_used": model,
            "output_video_url": f"/static/{output_filename}",
            "risk_level": risk_level,
            "summary": {
                "smoke_count": stats["smoke_frames"],
                "fire_count": stats["fire_frames"],
                "max_confidence": stats["max_confidence"],
            },
            **stats
        }
        _save_output_metadata(output_path, response_payload)
        return response_payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        try:
            if input_path.exists():
                input_path.unlink()
        except PermissionError:
            print(f"Warning: could not delete temp video {input_path}")
