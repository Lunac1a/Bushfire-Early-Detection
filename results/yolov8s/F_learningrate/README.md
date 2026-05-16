# F Group — Learning Rate Study

## 1. Objective

This experiment studies the effect of different learning rate strategies on the convergence behavior and final detection performance of the YOLOv8s wildfire detection model.

The purpose is to analyze:

- Training stability
- Convergence behavior
- mAP performance
- Precision and Recall balance
- Overall optimization effectiveness

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
- Seed: 42

### Learning Rate Groups

| Experiment | Learning Rate Strategy |
|---|---|
| F1 | Default Learning Rate |
| F2 | Lower Learning Rate |
| F3 | Cosine Learning Rate |

### Learning Rate Parameters

| Experiment | lr0 | lrf | cos_lr |
|---|---|---|---|
| F1 | 0.01 | 0.01 | False |
| F2 | 0.005 | 0.01 | False |
| F3 | 0.01 | 0.01 | True |

---

## 3. Quantitative Results

| Experiment | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| F1 (Default LR) | 0.779 | 0.723 | 0.778 | 0.454 |
| F2 (Lower LR) | 0.779 | 0.723 | 0.778 | 0.454 |
| F3 (Cosine LR) | 0.781 | 0.719 | 0.782 | 0.455 |

---

## 4. Training Curve Analysis

### F1 — Default Learning Rate

The default learning rate produced stable and smooth convergence behavior.

#### Observations

- Training loss steadily decreased throughout training
- Validation loss remained stable after convergence
- Precision and Recall improved consistently
- mAP50 and mAP50-95 gradually converged around epoch 35–40

The default learning rate achieved a good balance between convergence speed and final performance.

---

### F2 — Lower Learning Rate

The lower learning rate experiment produced almost identical results to the default learning rate configuration.

#### Observations

- Training curves were highly similar to F1
- Final Precision, Recall, and mAP values showed almost no difference
- No obvious improvement in convergence stability was observed

This indicates that reducing the initial learning rate from 0.01 to 0.005 had very limited impact under the current YOLOv8s training configuration.

---

### F3 — Cosine Learning Rate

The cosine learning rate strategy produced slightly different convergence behavior.

#### Observations

- Training curves remained smooth and stable
- Precision and mAP values were slightly higher than F1
- Later-stage convergence appeared slightly smoother
- Recall was slightly lower than F1

The cosine learning rate schedule slightly improved optimization performance, but the improvement was relatively small.

---

## 5. Confusion Matrix Analysis

### Smoke Detection

| Experiment | Smoke Accuracy |
|---|---|
| F1 | 0.85 |
| F2 | 0.85 |
| F3 | 0.83 |

The default learning rate maintained the highest smoke recognition accuracy.

---

### Fire Detection

| Experiment | Fire Accuracy |
|---|---|
| F1 | 0.73 |
| F2 | 0.73 |
| F3 | 0.74 |

F3 slightly improved fire detection accuracy.

---

### Background Predictions

All three experiments showed relatively similar background prediction behavior.

No abnormal false detection patterns were observed.

---

## 6. Learning Rate Discussion

This experiment shows that the YOLOv8s wildfire detection model is relatively stable under different learning rate strategies.

### Main Findings

- Lower learning rate did not significantly improve performance
- Cosine learning rate slightly improved mAP and Precision
- Default learning rate maintained better Recall and smoke detection stability

For wildfire smoke detection, Recall is important because missed smoke detections can be more critical than a small increase in false positives.

Therefore, maintaining stable smoke detection performance is more valuable than pursuing very small mAP improvements.

---

## 7. Final Conclusion

The F group experiments demonstrate that the current YOLOv8s configuration is not highly sensitive to learning rate changes.

Although the cosine learning rate strategy achieved slightly higher mAP values, the improvement was very small.

The default learning rate configuration achieved:

- More balanced Recall
- Better smoke detection accuracy
- Stable convergence behavior
- Reliable overall performance

Therefore, the project will continue using:

**Default Learning Rate (lr0 = 0.01)**

as the standard training setting for future experiments.