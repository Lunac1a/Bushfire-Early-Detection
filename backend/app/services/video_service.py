import cv2
import numpy as np


BOX_THICKNESS = 2
LABEL_FONT = cv2.FONT_HERSHEY_SIMPLEX
LABEL_SCALE = 0.55
LABEL_THICKNESS = 2
MIN_TRACK_POINTS = 4

CLASS_COLORS = {
    "fire": (68, 68, 239),
    "smoke": (93, 201, 244),
}


def _clamp_bbox(bbox, width: int, height: int):
    x1, y1, x2, y2 = bbox
    x1 = max(0.0, min(float(width - 1), x1))
    y1 = max(0.0, min(float(height - 1), y1))
    x2 = max(0.0, min(float(width - 1), x2))
    y2 = max(0.0, min(float(height - 1), y2))

    if x2 <= x1:
        x2 = min(float(width - 1), x1 + 1.0)
    if y2 <= y1:
        y2 = min(float(height - 1), y1 + 1.0)

    return [x1, y1, x2, y2]


def _bbox_to_roi(bbox, frame_shape):
    height, width = frame_shape[:2]
    x1, y1, x2, y2 = _clamp_bbox(bbox, width, height)

    left = max(0, int(np.floor(x1)))
    top = max(0, int(np.floor(y1)))
    right = min(width, int(np.ceil(x2)))
    bottom = min(height, int(np.ceil(y2)))

    if right - left < 2 or bottom - top < 2:
        return None

    return left, top, right, bottom


def _extract_track_points(gray_frame, bbox):
    roi = _bbox_to_roi(bbox, gray_frame.shape)
    if roi is None:
        return None

    left, top, right, bottom = roi
    region = gray_frame[top:bottom, left:right]
    points = cv2.goodFeaturesToTrack(
        region,
        maxCorners=30,
        qualityLevel=0.01,
        minDistance=6,
        blockSize=5,
    )

    if points is None:
        return None

    points[:, 0, 0] += left
    points[:, 0, 1] += top
    return points.astype(np.float32)


def _detection_to_track(box, names, frame_shape, gray_frame):
    cls_id = int(box.cls[0].item())
    confidence = float(box.conf[0].item())
    bbox = _clamp_bbox(box.xyxy[0].tolist(), frame_shape[1], frame_shape[0])
    class_name = names[cls_id]

    return {
        "bbox": bbox,
        "class_name": class_name,
        "confidence": confidence,
        "points": _extract_track_points(gray_frame, bbox),
    }


def _refresh_track_points(gray_frame, tracked_detection):
    tracked_detection["points"] = _extract_track_points(gray_frame, tracked_detection["bbox"])


def _track_detections(prev_gray, gray_frame, tracked_detections, frame_shape):
    updated = []

    for tracked_detection in tracked_detections:
        points = tracked_detection.get("points")
        if points is None or len(points) < MIN_TRACK_POINTS:
            _refresh_track_points(prev_gray, tracked_detection)
            points = tracked_detection.get("points")

        if points is None or len(points) < MIN_TRACK_POINTS:
            updated.append(tracked_detection)
            continue

        next_points, status, _ = cv2.calcOpticalFlowPyrLK(
            prev_gray,
            gray_frame,
            points,
            None,
            winSize=(21, 21),
            maxLevel=3,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.03),
        )

        if next_points is None or status is None:
            updated.append(tracked_detection)
            continue

        valid_mask = status.reshape(-1) == 1
        previous_valid = points[valid_mask]
        next_valid = next_points[valid_mask]

        if len(next_valid) < MIN_TRACK_POINTS:
            updated.append(tracked_detection)
            continue

        deltas = next_valid.reshape(-1, 2) - previous_valid.reshape(-1, 2)
        shift_x, shift_y = np.median(deltas, axis=0)

        x1, y1, x2, y2 = tracked_detection["bbox"]
        updated_bbox = _clamp_bbox(
            [x1 + shift_x, y1 + shift_y, x2 + shift_x, y2 + shift_y],
            frame_shape[1],
            frame_shape[0],
        )

        tracked_detection["bbox"] = updated_bbox
        tracked_detection["points"] = next_valid.reshape(-1, 1, 2).astype(np.float32)

        if len(tracked_detection["points"]) < 10:
            _refresh_track_points(gray_frame, tracked_detection)

        updated.append(tracked_detection)

    return updated


def _draw_detections(frame, tracked_detections):
    annotated = frame.copy()

    for tracked_detection in tracked_detections:
        x1, y1, x2, y2 = [int(round(value)) for value in tracked_detection["bbox"]]
        class_name = tracked_detection["class_name"]
        confidence = tracked_detection["confidence"]
        color = CLASS_COLORS.get(class_name.lower(), (141, 214, 56))

        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, BOX_THICKNESS)

        label = f"{class_name} {confidence:.2f}"
        label_size, baseline = cv2.getTextSize(label, LABEL_FONT, LABEL_SCALE, LABEL_THICKNESS)
        label_left = x1
        label_top = max(0, y1 - label_size[1] - baseline - 6)
        label_right = x1 + label_size[0] + 10
        label_bottom = label_top + label_size[1] + baseline + 6

        cv2.rectangle(annotated, (label_left, label_top), (label_right, label_bottom), color, -1)
        cv2.putText(
            annotated,
            label,
            (label_left + 5, label_bottom - baseline - 3),
            LABEL_FONT,
            LABEL_SCALE,
            (255, 255, 255),
            LABEL_THICKNESS,
            cv2.LINE_AA,
        )

    return annotated


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
    tracked_frames = 0
    max_confidence = 0.0
    smoke_frames = 0
    fire_frames = 0
    prev_gray = None
    tracked_detections = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if frame_index % frame_skip == 0:
            results = model(frame, conf=0.4)
            result = results[0] if isinstance(results, list) else results
            tracked_detections = []

            if result.boxes is not None and len(result.boxes) > 0:
                detected_frames += 1
                detected_smoke = False
                detected_fire = False
                for box in result.boxes:
                    tracked_detection = _detection_to_track(box, result.names, frame.shape, gray_frame)
                    tracked_detections.append(tracked_detection)
                    max_confidence = max(max_confidence, tracked_detection["confidence"])
                    if tracked_detection["class_name"].lower() == "smoke":
                        detected_smoke = True
                    elif tracked_detection["class_name"].lower() == "fire":
                        detected_fire = True
                if detected_smoke:
                    smoke_frames += 1
                if detected_fire:
                    fire_frames += 1
        elif tracked_detections and prev_gray is not None:
            tracked_detections = _track_detections(prev_gray, gray_frame, tracked_detections, frame.shape)
            tracked_frames += 1

        annotated_frame = _draw_detections(frame, tracked_detections) if tracked_detections else frame.copy()
        writer.write(annotated_frame)

        prev_gray = gray_frame
        frame_index += 1

    cap.release()
    writer.release()

    return {
        "total_frames": total_frames,
        "processed_frames": frame_index,
        "detected_frames": detected_frames,
        "tracked_frames": tracked_frames,
        "smoke_frames": smoke_frames,
        "fire_frames": fire_frames,
        "max_confidence": round(max_confidence, 4),
        "video_codec": selected_codec,
    }
