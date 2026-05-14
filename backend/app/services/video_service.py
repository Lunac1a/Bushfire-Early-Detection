import cv2
from fastapi import Query

from app.services.model_service import get_model


def process_video(
        input_path: str,
        output_path: str,
        model: str = Query("v8s"),
        frame_skip: int = 5
):
    yolo_model = get_model(model)

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError("Failed to open input video.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        annotated_frame = frame.copy()

        if frame_index % frame_skip == 0:
            results = yolo_model.predict(source=frame, conf=0.25, verbose=False)

            if results and len(results) > 0:
                result = results[0]
                boxes = result.boxes

                if boxes is not None and len(boxes) > 0:
                    annotated_frame = result.plot()

        writer.write(annotated_frame)
        frame_index += 1

    cap.release()
    writer.release()
