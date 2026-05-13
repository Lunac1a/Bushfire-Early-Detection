# B Group - Epoch Comparison Experiment

## Objective

This experiment investigates how different epoch settings affect the performance of the YOLOv8s wildfire smoke detection model.

After completing the A group image size experiments, the best image size (640×640) was selected and fixed for this stage. Only the number of training epochs was changed in this experiment.

---

# Experiment Settings

| Experiment | Epochs | Image Size | Batch Size | Model |
|---|---|---|---|---|
| B1 | 30 | 640 | 16 | YOLOv8s |
| B2 | 50 | 640 | 16 | YOLOv8s |
| B3 | 80 | 640 | 16 | YOLOv8s |

Common training settings:

- Pretrained: True
- AMP: True
- Workers: 8
- Seed: 42
- Device: NVIDIA Tesla T4

---

# Experiment Results

## B1 - 30 Epochs

### Analysis

The 30-epoch model achieved stable detection performance but did not fully converge. The training and validation losses were still decreasing near the end of training, and the mAP curves continued improving. This suggests that 30 epochs may be insufficient for fully learning wildfire smoke and fire features.

The confusion matrix showed that smoke detection already achieved relatively high accuracy, while fire detection performance remained lower and required additional training.

---

## B2 - 50 Epochs

### Analysis

The 50-epoch model achieved the best overall balance between performance and training efficiency. The loss curves became stable, while precision, recall, and mAP metrics reached smooth convergence without obvious overfitting.

Compared with the 30-epoch experiment, both smoke and fire detection became more stable, and the overall classification performance improved.

---

## B3 - 80 Epochs

### Analysis

The 80-epoch model slightly improved several metrics compared with the 50-epoch experiment. However, the improvement was limited relative to the increased training time. The model showed diminishing returns after around 50 epochs.

Although the training loss continued decreasing, the validation performance improved only slightly, indicating that additional epochs provided limited practical benefit.

---

# Comparison Analysis

| Experiment | Main Observation |
|---|---|
| B1 | Training was insufficient and the model had not fully converged |
| B2 | Best balance between accuracy and efficiency |
| B3 | Slight improvement but diminishing returns appeared |

Additional observations:

- Smoke detection achieved consistently high accuracy across all experiments.
- Fire detection required more training epochs for improvement.
- Some background regions were still incorrectly classified as smoke or fire due to complex environmental conditions.

---

# Conclusion

This experiment demonstrates that increasing the number of epochs can improve wildfire detection performance up to a certain point. However, excessive training epochs do not necessarily produce significant improvements.

Among all tested configurations, 50 epochs provided the best balance between detection accuracy, convergence stability, and computational efficiency.

---

# Best Configuration

| Parameter | Value |
|---|---|
| Model | YOLOv8s |
| Epochs | 50 |
| Image Size | 640 |
| Batch Size | 16 |
| Precision | ~0.79 |
| Recall | ~0.73 |
| mAP50 | ~0.79 |
| mAP50-95 | ~0.46 |