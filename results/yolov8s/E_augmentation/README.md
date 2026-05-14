# E Group — Augmentation Strategy Study

## 1. Objective

This experiment studies how different data augmentation strategies affect the performance and generalization ability of the YOLOv8s wildfire detection model.

Unlike the previous A/B/C/D experiments, the E group focuses more on:

- Generalization capability
- Smoke detection stability
- Small and distant smoke detection
- Complex background robustness
- Real-world deployment adaptability

Wildfire smoke is a difficult detection target because it often has:

- Blurry boundaries
- Weak texture features
- Large shape variations
- Semi-transparent appearance
- Strong similarity to clouds and fog

Therefore, this experiment investigates whether different augmentation strategies can improve wildfire smoke detection performance.

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
| E1 | Default Augmentation |
| E2 | Strong Augmentation |
| E3 | Reduced Mosaic Strategy |

---

## 4. Augmentation Parameter Design

### E1 — Default Augmentation

E1 uses the default YOLOv8 augmentation pipeline.

The default augmentation strategy includes:

- Mosaic augmentation
- HSV color augmentation
- Random scaling
- Random flipping
- Random translation

The purpose of E1 is to serve as the baseline reference for later augmentation comparisons.

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

- Lighting variation
- Weather changes
- Camera movement
- Distant smoke targets
- Complex wildfire scenes

However, stronger augmentation may also introduce:

- Texture distortion
- More difficult optimization
- Unrealistic smoke structures

This is especially important for smoke detection because smoke has soft texture and unclear boundaries.

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

Unlike rigid objects such as vehicles or humans, wildfire smoke is highly deformable and semi-transparent.

Heavy Mosaic augmentation may:

- Break smoke texture continuity
- Distort smoke boundaries
- Remove small smoke regions
- Create unrealistic smoke patterns

Therefore, E3 reduces Mosaic intensity while keeping moderate augmentation ability.

The purpose is to preserve more realistic smoke texture information during training.

---

## 5. Quantitative Results

| Experiment | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| E1 (Default Aug) | 0.789 | 0.724 | 0.789 | 0.457 |
| E2 (Strong Aug) | 0.771 | 0.739 | 0.787 | 0.456 |
| E3 (Reduced Mosaic) | 0.786 | 0.713 | 0.782 | 0.451 |

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

This suggests that stronger augmentation improved the model’s sensitivity to difficult wildfire smoke targets.

Possible improvements include:

- Better distant smoke detection
- Stronger adaptability to lighting variation
- Improved robustness under complex scenes

However, Precision slightly decreased.

This indicates that the model became more aggressive and produced more unstable predictions.

---

### E3 — Reduced Mosaic Strategy

E3 maintained relatively stable performance but did not outperform the default augmentation strategy.

Although reducing Mosaic intensity helped preserve smoke texture continuity, the improvement was limited on the current dataset.

This suggests that the default YOLOv8 augmentation pipeline is already suitable for the wildfire smoke dataset.

---

## 8. Confusion Matrix Analysis

### Smoke Detection

| Experiment | Smoke Accuracy |
|---|---|
| E1 | 0.85 |
| E2 | 0.83 |
| E3 | 0.84 |

E1 achieved the best smoke classification stability.

E2 slightly reduced smoke detection accuracy, likely because aggressive augmentation distorted smoke texture features.

E3 maintained stable smoke detection performance after reducing Mosaic intensity.

---

### Fire Detection

| Experiment | Fire Accuracy |
|---|---|
| E1 | 0.73 |
| E2 | 0.73 |
| E3 | 0.71 |

E1 and E2 achieved similar fire detection performance.

E3 showed a small decrease in fire classification accuracy.

---

### Background Predictions

E2 produced slightly more aggressive background predictions.

This behavior is consistent with its higher Recall performance.

The stronger augmentation increased model sensitivity, but also introduced slightly more unstable predictions.

---

## 9. Discussion

The E group experiments demonstrate that augmentation strategy has a clear influence on wildfire smoke detection behavior.

Key findings include:

- Strong augmentation improved Recall slightly
- Excessive augmentation introduced more unstable smoke predictions
- Reduced Mosaic augmentation maintained stable performance
- The default YOLOv8 augmentation pipeline achieved the best overall balance

The results also suggest that the wildfire smoke dataset may already contain sufficient environmental diversity, reducing the benefit of stronger augmentation strategies.

Compared with rigid object detection tasks, wildfire smoke detection requires careful augmentation design because smoke is:

- Semi-transparent
- Shape-changing
- Texture-sensitive
- Easily affected by image transformations

---

## 10. Final Conclusion

The E group experiments confirm that augmentation strategy affects wildfire smoke detection performance.

### Main Conclusions

- E2 slightly improved Recall and generalization ability
- E2 also introduced more unstable smoke predictions
- E3 maintained stable smoke texture learning
- E1 achieved the best overall performance balance

The results suggest that:

> More aggressive augmentation is not always better for wildfire smoke detection.

Among all augmentation strategies, the default YOLOv8 augmentation pipeline achieved the best balance between:

- Precision
- Recall
- mAP performance
- Smoke classification stability

Therefore, the project will continue using the default YOLOv8 augmentation strategy for later experiments.

### Current Best Augmentation Configuration

Default YOLOv8 augmentation settings:

- mosaic = default
- hsv augmentation = default
- scale = default
- flip = default
- translation = default