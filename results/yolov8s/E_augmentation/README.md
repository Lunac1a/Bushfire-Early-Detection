# E Group — Augmentation Strategy Study

## 1. Objective

This experiment studies how different data augmentation strategies affect the generalization ability and detection stability of the YOLOv8s wildfire detection model.

Unlike the previous A/B/C/D experiments, the E group focuses more on:

- Generalization capability
- Smoke detection stability
- Small and distant smoke detection
- Complex background robustness
- Real-world deployment adaptability

Wildfire smoke is a challenging detection target because it often has:

- Blurry boundaries
- Weak texture features
- Large shape variations
- Semi-transparent appearance
- Strong similarity to clouds and fog

Therefore, this experiment investigates whether different augmentation strategies can improve the model’s robustness in complex wildfire monitoring scenarios.

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

---

## 3. Augmentation Groups

| Experiment | Strategy |
|---|---|
| E1 | Default Augmentation (Baseline) |
| E2 | Strong Augmentation |
| E3 | Reduced Mosaic Strategy |

---

## 4. Augmentation Parameter Design

### E1 — Default Augmentation

E1 reuses the current best baseline configuration without additional retraining.

This configuration uses the default YOLOv8 augmentation pipeline, including:

- Mosaic augmentation
- HSV color augmentation
- Random scaling
- Random flipping
- Random translation

The purpose of E1 is to serve as the reference baseline for later augmentation comparisons.

---

### E2 — Strong Augmentation

E2 applies a more aggressive augmentation strategy.

### Modified Parameters

| Parameter | Value |
|---|---|
| mosaic | 1.0 |
| close_mosaic | 10 |
| hsv_h | 0.015 |
| hsv_s | 0.8 |
| hsv_v | 0.5 |
| scale | 0.7 |
| translate | 0.1 |
| fliplr | 0.5 |

### Design Purpose

The goal of E2 is to improve model generalization under difficult wildfire monitoring conditions.

The stronger augmentation simulates:

- Different lighting conditions
- Weather changes
- Camera movement
- Distant smoke targets
- Complex backgrounds

However, stronger augmentation may also introduce:

- Texture distortion
- More aggressive transformations
- Harder optimization during training

This is especially important for smoke detection because smoke is a soft-texture object with unclear boundaries.

---

### E3 — Reduced Mosaic Strategy

E3 reduces the intensity of Mosaic augmentation.

### Modified Parameters

| Parameter | Value |
|---|---|
| mosaic | 0.5 |
| close_mosaic | 20 |
| hsv_h | 0.015 |
| hsv_s | 0.7 |
| hsv_v | 0.4 |
| scale | 0.5 |
| fliplr | 0.5 |

### Design Purpose

Unlike rigid objects such as cars or people, wildfire smoke is highly deformable and semi-transparent.

Heavy Mosaic augmentation may:

- Break smoke texture continuity
- Distort smoke boundaries
- Remove small smoke regions
- Create unrealistic smoke patterns

Therefore, E3 reduces Mosaic intensity while keeping moderate augmentation ability.

The purpose is to help the model learn more realistic smoke texture and boundary features.

---

## 5. Quantitative Results

| Experiment | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| E1 (Default Aug) | 0.786 | 0.713 | 0.782 | 0.451 |
| E2 (Strong Aug) | 0.770 | 0.739 | 0.786 | 0.456 |
| E3 (Reduced Mosaic) | 0.792 | 0.726 | 0.788 | 0.458 |

---

## 6. Training Curve Analysis

All augmentation experiments showed stable convergence behavior.

### Observations

- Training losses decreased steadily
- Validation losses remained stable after convergence
- No abnormal oscillation was observed
- Precision and Recall improved consistently during training
- mAP50 and mAP50-95 curves converged smoothly

The results indicate that all augmentation strategies were trainable and did not destabilize the YOLOv8s optimization process.

---

## 7. Recall and Generalization Analysis

### E2 — Strong Augmentation

E2 achieved the highest Recall among all augmentation experiments.

This suggests that stronger augmentation improved the model’s ability to discover difficult wildfire smoke targets.

Possible improvements include:

- Better distant smoke detection
- Stronger robustness under lighting variation
- Improved adaptability to complex scenes

However, Precision slightly decreased.

This indicates that the model became more sensitive and produced more aggressive predictions.

---

### E3 — Reduced Mosaic Strategy

E3 achieved a better balance between Precision and Recall.

Compared with E2:

- Precision increased
- Smoke classification stability improved
- mAP50-95 achieved the best result

This suggests that reducing Mosaic intensity may be more suitable for wildfire smoke detection.

---

## 8. Confusion Matrix Analysis

### Smoke Detection

| Experiment | Smoke Accuracy |
|---|---|
| E1 | 0.84 |
| E2 | 0.83 |
| E3 | 0.85 |

E3 achieved the best smoke detection stability.

This result supports the hypothesis that excessive Mosaic augmentation may damage smoke texture features.

Reducing Mosaic intensity allows the model to learn more realistic smoke structures.

---

### Fire Detection

| Experiment | Fire Accuracy |
|---|---|
| E1 | 0.71 |
| E2 | 0.73 |
| E3 | 0.73 |

Both E2 and E3 improved fire detection performance.

This indicates that augmentation helped improve model generalization for fire-related patterns.

---

### Background Predictions

E2 showed slightly more aggressive background predictions.

This is consistent with its higher Recall performance.

Meanwhile, E3 maintained stronger smoke classification stability while keeping background prediction behavior relatively clean.

---

## 9. Discussion

The E group experiments demonstrate that augmentation strategy has a clear impact on wildfire smoke detection behavior.

Key findings include:

- Strong augmentation improves Recall and generalization ability
- Excessive augmentation may slightly reduce Precision
- Wildfire smoke may not benefit from overly aggressive Mosaic augmentation
- Reduced Mosaic intensity improves smoke texture learning and detection stability

Compared with rigid object detection tasks, wildfire smoke detection requires more careful augmentation design because smoke is:

- Semi-transparent
- Shape-changing
- Texture-sensitive
- Easily distorted by image stitching operations

Among all augmentation strategies, E3 achieved the best overall balance between:

- Precision
- Recall
- mAP performance
- Smoke classification stability

---

## 10. Final Conclusion

The E group experiments confirm that augmentation strategy plays an important role in wildfire smoke detection performance.

### Main Conclusions

- E2 improved Recall and generalization ability through stronger augmentation
- E3 achieved the best overall performance by reducing Mosaic intensity
- Reduced Mosaic augmentation appears to be more suitable for smoke-style targets

The results suggest that:

> Stronger augmentation is not always better for wildfire smoke detection.

Instead, carefully controlled augmentation may produce more stable and realistic feature learning.

Based on the E group results, the project will continue using the E3 augmentation strategy for later optimization experiments.

### Current Best Augmentation Configuration

- mosaic = 0.5
- close_mosaic = 20
- hsv_h = 0.015
- hsv_s = 0.7
- hsv_v = 0.4
- scale = 0.5
- fliplr = 0.5