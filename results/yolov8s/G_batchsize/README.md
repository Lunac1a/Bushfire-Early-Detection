# G Group — Batch Size Study

## 1. Objective

This experiment studies the impact of different batch sizes on YOLOv8s wildfire smoke and fire detection performance.

The purpose is to analyze how batch size affects:

- Training stability
- Convergence behavior
- Precision and Recall balance
- mAP performance
- Generalization ability
- GPU utilization efficiency

This experiment also evaluates whether larger batch sizes can improve training smoothness and overall detection consistency.

---

## 2. Experiment Settings

### Base Configuration

- Model: YOLOv8s
- Image Size: 640
- Epochs: 50
- Confidence Threshold: 0.25
- IoU Threshold: 0.5
- AMP: True
- Pretrained: True
- Seed: 42

### Batch Size Groups

| Experiment | Batch Size |
|---|---|
| G1 | 16 |
| G2 | 24 |
| G3 | 32 |

---

## 3. Quantitative Results

| Experiment | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| G1 (Batch 16) | 0.785 | 0.726 | 0.789 | 0.460 |
| G2 (Batch 24) | 0.792 | 0.735 | 0.787 | 0.460 |
| G3 (Batch 32) | 0.785 | 0.733 | 0.786 | 0.456 |

---

## 4. Training Curve Analysis

All three experiments showed stable convergence behavior.

### G1 — Batch Size 16

- Training and validation losses decreased steadily
- mAP performance was strong throughout training
- Slight fluctuations appeared during later epochs
- Overall convergence was stable

### G2 — Batch Size 24

- Training curves became smoother compared with G1
- Precision and Recall fluctuations were reduced
- Validation loss remained more stable during later epochs
- Recall slightly improved compared with G1

### G3 — Batch Size 32

- Training curves were the smoothest among all experiments
- Loss convergence remained highly stable
- However, mAP improvement became saturated
- Larger batch size did not further improve generalization performance

---

## 5. Confusion Matrix Analysis

The normalized confusion matrices of all three experiments were highly similar.

### Smoke Detection

- Smoke detection accuracy remained around 0.83–0.85
- All batch sizes maintained strong smoke detection capability

### Fire Detection

- Fire detection accuracy remained around 0.73–0.74
- No major differences between experiments

### Background Predictions

- Background false detections remained relatively stable
- Larger batch sizes did not significantly reduce background confusion

---

## 6. Batch Size Discussion

The results show that increasing batch size improves training smoothness and convergence stability.

### Observations

- Larger batch sizes reduced training noise
- Precision and Recall curves became smoother
- GPU utilization efficiency improved
- Recall slightly improved with larger batches

However, increasing batch size beyond a certain point did not continue improving detection performance.

### G2 vs G3

Compared with Batch Size 24:

- Batch Size 32 achieved smoother convergence
- But mAP50 and mAP50-95 did not improve further
- Slight generalization saturation began to appear

This suggests that excessively large batch sizes may reduce training noise too much, limiting further performance gains.

---

## 7. Final Conclusion

The G group experiments demonstrate that batch size has a noticeable influence on training stability and convergence behavior.

Among all settings:

- Batch Size 16 achieved strong baseline performance
- Batch Size 24 provided the best balance between:
  - Precision
  - Recall
  - Convergence stability
  - Overall detection performance
- Batch Size 32 improved smoothness further but did not improve final mAP performance

Therefore, the project selects:

**Batch Size = 24**

as the preferred batch size setting for future YOLOv8s wildfire detection experiments.