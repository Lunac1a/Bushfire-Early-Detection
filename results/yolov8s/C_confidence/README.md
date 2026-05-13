# C Group — Confidence Threshold Study

## 1. Objective

This experiment studies how different confidence thresholds affect wildfire smoke and fire detection performance in YOLOv8s.

The purpose is to analyze the trade-off between detection sensitivity and false positive reduction during inference.

---

## 2. Experiment Settings

### Base Model

- Model: YOLOv8s
- Best Weights: B2_epoch50/best.pt   #yolov8s_B2.pt
- Image Size: 640
- IoU Threshold: 0.5

### Confidence Threshold Groups

| Experiment | Confidence Threshold |
|---|---|
| C1 | 0.25 |
| C2 | 0.50 |
| C3 | 0.70 |

---

## 3. Quantitative Results

| Experiment | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| C1 (0.25) | 0.782 | 0.740 | 0.709 | 0.416 |
| C2 (0.50) | 0.873 | 0.631 | 0.600 | 0.370 |
| C3 (0.70) | 0.952 | 0.416 | 0.409 | 0.273 |

---

## 4. Qualitative Comparison

Example prediction comparison images are stored in the `compare_samples` folder.

The comparison images clearly show the effect of different confidence thresholds:

- Lower confidence thresholds detect more smoke and fire regions
- Higher confidence thresholds reduce extra predictions
- Very high confidence thresholds may miss important wildfire targets

### Observations

#### C1 — Confidence 0.25

- Highest Recall and best mAP performance
- Detects more small or unclear fire regions
- More prediction boxes may appear

#### C2 — Confidence 0.50

- Better balance between Precision and Recall
- Cleaner predictions than C1
- Some small targets are missed

#### C3 — Confidence 0.70

- Highest Precision
- Very strict prediction filtering
- Significant increase in missed detections

---

## 5. Analysis

The experiment shows a clear trade-off between Precision and Recall.

As the confidence threshold increases:

- Precision increases
- Recall decreases
- mAP performance drops

For wildfire detection tasks, missing smoke or fire regions can be more dangerous than having several extra predictions.

Therefore, lower confidence thresholds are more suitable for early wildfire detection systems.

---

## 6. Final Conclusion

Among the three confidence thresholds, C1 (confidence = 0.25) achieved the best overall detection performance.

Although C3 produced cleaner prediction results, it caused many missed detections and reduced Recall significantly.

Therefore, this project recommends:

**Confidence Threshold = 0.25**

for the final wildfire smoke detection deployment setting.