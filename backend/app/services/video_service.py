import cv2


def precess_video(
        input_path: str,
        output_path: str,
        model,
        frame_skip: int = 5
):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise ValueError("Failed to open input video.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0:
        fps = 25.0

    codec_candidates = ("avc1", "H264", "mp4v")
    writer = None
    selected_codec = None

    for codec in codec_candidates:
        fourcc = cv2.VideoWriter_fourcc(*codec)
        candidate = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        if candidate.isOpened():
            writer = candidate
            selected_codec = codec
            break
        candidate.release()

    if writer is None:
        cap.release()
        raise ValueError("Failed to create output video writer.")

    frame_index = 0
    detected_frames = 0
    max_confidence = 0.0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        annotated_frame = frame.copy()

        if frame_index % frame_skip == 0:
            results = model(frame, conf=0.4)
            result = results[0] if isinstance(results, list) else results

            if result.boxes is not None and len(result.boxes) > 0:
                detected_frames += 1
                annotated_frame = result.plot()

                for box in result.boxes:
                    confidence = float(box.conf[0].item())
                    max_confidence = max(max_confidence, confidence)

        writer.write(annotated_frame)
        frame_index += 1

    cap.release()
    writer.release()

    return {
        "total_frames": total_frames,
        "processed_frames": frame_index,
        "detected_frames": detected_frames,
        "max_confidence": round(max_confidence, 4),
        "video_codec": selected_codec,
    }
