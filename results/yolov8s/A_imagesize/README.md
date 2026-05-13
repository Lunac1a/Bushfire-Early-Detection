# A Group - Image Size Comparison Experiment

## Objective

This experiment investigates how different image sizes affect the performance of the YOLOv8s wildfire smoke detection model.

The image resolution directly influences feature extraction quality, computational cost, and detection accuracy. Three different image sizes were tested while keeping all other training settings unchanged.

---

# Experiment Settings

| Experiment | Image Size | Epochs | Batch Size | Model |
|---|---|---|---|---|
| A1 | 512 × 512 | 50 | 16 | YOLOv8s |
| A2 | 640 × 640 | 50 | 16 | YOLOv8s |
| A3 | 768 × 768 | 50 | 16 | YOLOv8s |

Common training settings:

- Pretrained: True
- AMP: True
- Workers: 8
- Seed: 42
- Device: NVIDIA Tesla T4

---

# Experiment Results

## A1 - 512 × 512

### Analysis

The 512×512 model achieved stable detection performance with relatively fast training speed and lower computational cost. However, smaller image resolution limited the model’s ability to capture detailed wildfire smoke and fire features, especially for small or distant targets.

The confusion matrix showed that some smoke and fire regions were still confused with background areas.

---

## A2 - 640 × 640

### Analysis

The 640×640 model achieved the best overall detection performance among all experiments. The training process remained stable, while precision, recall, and mAP metrics improved compared with the 512×512 experiment.

The higher image resolution allowed the model to capture more detailed smoke and fire features without introducing significant instability or excessive computational cost.

---

## A3 - 768 × 768

### Analysis

The 768×768 model further increased image detail, but the performance improvement was limited compared with the additional computational cost. Training time and GPU memory usage increased noticeably, while the overall detection metrics showed only small improvements.

This suggests that excessively large image sizes may not always provide practical benefits for this wildfire detection dataset.

---

# Comparison Analysis

| Experiment | Main Observation |
|---|---|
| A1 | Faster training but limited feature detail |
| A2 | Best balance between accuracy and efficiency |
| A3 | Higher computational cost with limited improvement |

Additional observations:

- Increasing image size improved the detection of small smoke and fire regions.
- Larger image sizes required longer training time and higher GPU memory usage.
- Excessively large image sizes did not significantly improve overall detection performance.

---

# Conclusion

This experiment demonstrates that image size has a significant impact on wildfire detection performance. Smaller image sizes reduce computational cost but may limit feature extraction capability, while excessively large image sizes increase training complexity without providing major performance gains.

Among all tested configurations, the 640×640 setting achieved the best balance between detection accuracy, training stability, and computational efficiency.

---

# Best Configuration

| Parameter | Value |
|---|---|
| Model | YOLOv8s |
| Image Size | 640 × 640 |
| Epochs | 50 |
| Batch Size | 16 |
| Precision | ~0.79 |
| Recall | ~0.73 |
| mAP50 | ~0.79 |
| mAP50-95 | ~0.46 |