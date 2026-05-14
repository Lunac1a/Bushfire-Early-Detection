# D Group — Seed Stability Study

## 1. Objective

This experiment studies the stability and reproducibility of the YOLOv8s wildfire detection model under different random seeds.

The purpose is to verify whether the current best configuration can produce stable results across multiple training runs.

---

## 2. Experiment Settings

### Base Configuration

- Model: YOLOv8s
- Image Size: 640
- Epochs: 50
- Batch Size: 16
- Confidence Threshold: 0.25
- IoU Threshold: 0.5
- AMP: True
- Pretrained: True

### Seed Groups

| Experiment | Random Seed |
|---|---|
| D1 | 42 |
| D2 | 43 |
| D3 | 44 |

---

## 3. Quantitative Results

| Experiment | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| D1 (Seed 42) | 0.789 | 0.724 | 0.787 | 0.455 |
| D2 (Seed 43) | 0.791 | 0.726 | 0.788 | 0.458 |
| D3 (Seed 44) | 0.803 | 0.719 | 0.789 | 0.457 |

---

## 4. Training Curve Analysis

The training curves of all three experiments show highly consistent behavior.

### Observations

- Training loss decreased steadily in all runs
- Validation loss remained stable after convergence
- Precision and Recall followed very similar trends
- mAP50 and mAP50-95 curves almost overlapped

The results indicate that the current YOLOv8s configuration has strong training stability.

---

## 5. Confusion Matrix Analysis

The normalized confusion matrices of D1, D2, and D3 are highly similar.

### Smoke Detection

- Smoke detection accuracy remained around 0.83–0.85
- Very small fluctuations between different seeds

### Fire Detection

- Fire detection accuracy remained around 0.73–0.74
- No obvious instability or class imbalance was observed

### Background Predictions

- Background false detections remained relatively stable
- No seed produced abnormal prediction behavior

---

## 6. Stability Discussion

This experiment demonstrates that the current best YOLOv8s configuration is reproducible and not dependent on a specific random seed.

Compared with previous A/B/C parameter tuning experiments, the D group focuses more on:

- Stability validation
- Reproducibility analysis
- Reliability of training results

The small performance differences between D1, D2, and D3 indicate that the model has good robustness during training.

---

## 7. Final Conclusion

The D group experiments confirm that the current YOLOv8s wildfire detection configuration is stable across different random seeds.

All three experiments achieved very similar:

- Precision
- Recall
- mAP50
- mAP50-95
- Confusion matrix patterns

Therefore, the current training configuration is considered reliable for later deployment and further optimization experiments.

The project will continue using:

**Seed = 42**

as the default training setting for future experiments.