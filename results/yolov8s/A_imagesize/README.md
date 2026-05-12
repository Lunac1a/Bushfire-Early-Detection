# A Group – Image Size Study

## Objective

This experiment investigates how different input image sizes affect the performance of the YOLOv8s wildfire detection model.

The study focuses on:
- Detection accuracy
- Training stability
- Small object detection ability
- Computational cost

---

## Experimental Settings

| Experiment | Image Size |
|---|---|
| A1 | 512 × 512 |
| A2 | 640 × 640 (Baseline) |
| A3 | 768 × 768 |

### Fixed Parameters

- Model: YOLOv8s
- Epochs: 50
- Batch Size: 16
- GPU: NVIDIA Tesla T4
- Dataset: Wildfire Smoke & Fire Dataset

---

## Key Findings

- Increasing image size improved feature representation slightly.
- However, performance gain beyond 640×640 was limited.
- A2 (640×640) achieved the best balance between:
  - accuracy
  - training stability
  - computational cost

---

## Final Conclusion

640×640 was selected as the optimal image size for the YOLOv8s wildfire detection model.

---

## Folder Structure

- `A1_imgsz512/`
- `A2_imgsz640/`
- `A3_imgsz768/`

Each folder contains:
- training curves
- confusion matrix
- evaluation results
- trained weights