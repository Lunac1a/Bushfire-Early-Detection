# Final Group — Final YOLOv8s Optimization Study

## 1. Objective

This final experiment stage focuses on exploring the strongest possible YOLOv8s wildfire smoke and fire detection configuration based on all previous experimental conclusions.

After completing the baseline experiment and Groups A–G studies, the project identified the following optimized configuration:

- Image Size = 640
- Epochs = 50
- Batch Size = 24
- Default YOLOv8 augmentation
- Default learning rate
- Confidence Threshold = 0.25

The purpose of the Final Group experiments is to further investigate whether:

- Longer training can improve model performance
- Additional epochs can improve small smoke detection
- Early stopping can improve convergence stability
- The model can achieve stronger generalization performance
- Further optimization can improve deployment-oriented wildfire detection quality

This stage focuses not only on mAP improvement, but also on:

- Detection stability
- Smoke detection consistency
- False positive reduction
- Recall performance
- Real-world deployment suitability

---

## 2. Experiment Settings

### Base Configuration

- Model: YOLOv8s
- Image Size: 640
- Batch Size: 24
- Confidence Threshold: 0.25
- IoU Threshold: 0.5
- AMP: True
- Pretrained: True
- Seed: 42

---

## 3. Final Experiment Groups

| Experiment | Configuration |
|---|---|
| Final1 | Best configuration confirmation (50 epochs) |
| Final2 | Batch 24 + 80 epochs |
| Final3 | Batch 24 + 100 epochs with Early Stopping |

---

## 4. Quantitative Results

| Experiment | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| Final1 | 0.767 | 0.728 | 0.783 | 0.458 |
| Final2 | 0.796 | 0.721 | 0.789 | **0.463** |
| Final3 | **0.801** | 0.714 | **0.795** | 0.462 |

---

## 5. Training Curve Analysis

All three experiments showed stable convergence behavior without severe overfitting.

---

### Final1 — Best Configuration Confirmation

- Training and validation losses decreased steadily
- Precision and Recall curves remained smooth
- mAP curves converged stably during later epochs
- The experiment confirmed that the optimized Batch Size 24 configuration was highly reproducible

However:

- Performance improvement began saturating near the end of training
- Final mAP50-95 remained slightly lower than the later long-training experiments

---

### Final2 — Extended Training (80 Epochs)

Final2 achieved the strongest overall balance among all final experiments.

Observations:

- Longer training further improved feature learning
- Smoke detection accuracy improved compared with Final1
- mAP50-95 achieved the highest overall result
- Precision and Recall remained stable during later epochs
- No severe overfitting behavior appeared

Compared with Final1:

- Smoke detection performance improved
- Background confusion slightly decreased
- Model convergence became more mature and stable

This suggests that the optimized YOLOv8s configuration still benefited from moderate additional training.

---

### Final3 — Long Training with Early Stopping

Final3 introduced Early Stopping to automatically determine the optimal stopping point.

The model stopped training at Epoch 73.

Observations:

- Precision achieved the highest value among all experiments
- mAP50 also achieved the highest result
- Training curves remained smooth and highly stable
- Early stopping successfully prevented unnecessary late-stage training

However:

- Recall slightly decreased compared with Final2
- mAP50-95 remained marginally lower than Final2
- Smoke detection consistency was slightly weaker than Final2

This indicates that stronger precision optimization slightly reduced overall recall performance.

---

## 6. Confusion Matrix Analysis

### Smoke Detection

Final2 achieved the strongest smoke detection performance.

| Experiment | Smoke Accuracy |
|---|---|
| Final1 | 0.83 |
| Final2 | **0.85** |
| Final3 | 0.84 |

Observations:

- Final2 produced the strongest smoke recognition capability
- Background-to-smoke confusion slightly decreased
- Small and distant smoke detection became more stable

---

### Fire Detection

All three experiments achieved similar fire detection performance.

| Experiment | Fire Accuracy |
|---|---|
| Final1 | 0.73 |
| Final2 | 0.75 |
| Final3 | 0.75 |

The model maintained strong fire classification consistency across all configurations.

---

### Background Predictions

Background false detections remained one of the primary challenges of wildfire smoke detection.

This is expected because:

- Clouds
- Fog
- Bright sky regions
- Low-contrast smoke

often share visual similarities with wildfire smoke.

However:

- Final2 achieved the best overall balance between smoke detection and background confusion
- Final3 slightly reduced fire false positives but increased smoke background confusion

---

## 7. Final Optimization Discussion

The Final Group experiments demonstrate that the YOLOv8s wildfire detection model had not fully saturated after 50 epochs.

### Key Findings

- Batch Size 24 remained highly effective
- Moderate longer training improved feature learning
- Extended training improved smoke detection quality
- Early stopping improved training efficiency and stability
- Extremely long training did not provide major additional gains

---

### Final2 vs Final3

Final3 achieved:

- Highest Precision
- Highest mAP50

However:

- Recall slightly decreased
- Smoke detection consistency weakened slightly

For wildfire smoke detection systems, Recall and smoke sensitivity are especially important because missing smoke detections can be more harmful than occasional false positives.

Therefore:

- Final2 achieved the strongest overall deployment-oriented balance
- Final2 provided better smoke detection robustness
- Final2 achieved the best overall mAP50-95 performance

---

## 8. Final Conclusion

The Final Group experiments successfully identified the strongest YOLOv8s configuration for this project.

Among all experiments:

- Final1 confirmed the stability of the optimized configuration
- Final3 demonstrated the effectiveness of early stopping
- Final2 achieved the best overall balance between:
  - Precision
  - Recall
  - Smoke detection capability
  - Generalization performance
  - Convergence stability
  - Deployment suitability

Therefore, the project selects:

# Final YOLOv8s Wildfire Detection Model

- Model: YOLOv8s
- Image Size: 640
- Epochs: 80
- Batch Size: 24
- Confidence Threshold: 0.25
- IoU Threshold: 0.5
- AMP: True
- Pretrained: True
- Seed: 42

Final selected model:

```python
Final2_batch24_epoch80
```

This model achieved the strongest overall wildfire smoke and fire detection performance across all experiments conducted in this project.