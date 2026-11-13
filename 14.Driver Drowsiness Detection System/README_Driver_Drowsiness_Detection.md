# Driver Drowsiness Detection System

A computer-vision project that classifies a driver's facial image as **Drowsy** or **Non-Drowsy** using transfer learning with MobileNetV2. The notebook demonstrates face detection, image augmentation, two-phase training, model evaluation, TensorFlow Lite conversion, quantization, and lightweight-model inference.

> **Safety note:** This is an educational prototype, not a certified driver-monitoring or vehicle-safety system. It must not be used as the sole basis for real-world driving decisions without extensive validation, fail-safe design, and applicable safety/regulatory review.

## 1. Problem statement

Driver fatigue is a significant road-safety risk, particularly in commercial transport and long-haul driving. Continuous manual monitoring is difficult to scale, while simple rule-based alerts may not reliably identify early signs of drowsiness.

This project explores an AI-based approach that analyses facial images and predicts whether the driver is drowsy. The intended deployment direction is an edge device, where a compact model can support timely driver alerts.

## 2. Objectives

- Classify facial images into two classes: `Non-Drowsy` and `Drowsy`.
- Inspect and understand the image dataset before training.
- Demonstrate face detection and face-region cropping using Dlib and OpenCV.
- Improve robustness through image preprocessing and augmentation.
- Apply transfer learning with an ImageNet-pretrained MobileNetV2.
- Train in two phases: frozen feature extractor, followed by selective fine-tuning.
- Evaluate with accuracy, precision, recall, F1-score, classification report, and confusion matrix.
- Examine false negatives and decision-threshold behaviour.
- Convert the trained model to TensorFlow Lite and compare Float32, Float16, and INT8 model sizes.
- Demonstrate inference using a TensorFlow Lite model.

## 3. Project workflow

```text
Image Dataset
     |
     v
Dataset Inspection and Sample Visualization
     |
     v
Face Detection / Face Crop Demonstration
(Dlib and OpenCV)
     |
     v
Train / Validation / Test Dataset Creation
     |
     v
Preprocessing and Data Augmentation
     |
     v
MobileNetV2 Transfer Learning
     |
     +--> Phase 1: Freeze pretrained base; train classifier head
     |
     +--> Phase 2: Unfreeze selected upper layers; fine-tune
     |
     v
Training Curves and Test Evaluation
     |
     v
Confusion Matrix / False-Negative / Threshold Analysis
     |
     v
TensorFlow Lite Conversion and Quantization
     |
     v
TFLite Inference and Model-Size Comparison
```

## 4. Dataset

The project uses the [Driver Drowsiness Detection Systems Dataset](https://drive.google.com/file/d/1Z8VTDfzAgz67j6u3FKBmdpWG16xiESJB/view?usp=sharing).

The notebook expects the following directory layout:

```text
driver-drowsiness/
└── dataset/
    ├── train/
    │   ├── Drowsy/
    │   └── Non-Drowsy/
    └── test/
        ├── Drowsy/
        └── Non-Drowsy/
```

The class mapping used in the notebook is:

| Class | Label |
|---|---:|
| Non-Drowsy | 0 |
| Drowsy | 1 |

The notebook includes an optional Google Drive download/extraction section. If the dataset is already available locally or in the notebook runtime, configure `DATASET_DIR` to point to its `dataset` folder.

**Data-splitting guidance:** Keep the supplied test set separate from training and model selection. Use only the training partition to create training and validation subsets. Where multiple images come from the same driver or recording session, prefer a driver/session-level split to reduce data leakage.

## 5. Notebook contents

The main notebook is:

`driver-drowsiness-mobilenetv2-complete-final.ipynb`

It is organized into the following stages:

1. Install and import libraries.
2. Optional dataset download and extraction.
3. Dataset configuration and inspection.
4. Visualize sample images.
5. Dlib face-detection demonstration.
6. OpenCV Haar Cascade face-detection demonstration.
7. Batch face-detection quality analysis.
8. Build training, validation, and test datasets.
9. Image augmentation.
10. MobileNetV2 transfer-learning model.
11. Phase 1 — train the classification head with the base model frozen.
12. Phase 2 — fine-tune selected upper layers with a lower learning rate.
13. Training and validation curves.
14. Final test evaluation.
15. Confusion matrix.
16. Decision-threshold analysis.
17. False-negative analysis.
18. TensorFlow Lite Float32 conversion.
19. Float16 quantization.
20. INT8 quantization.
21. TFLite inference demonstration.
22. Model-size comparison.
23. Business-question answers and deployment recommendation.
24. Model download utilities and submission checklist.

### Face detection note

The notebook explains that the supplied dataset already contains cropped face images. Dlib and OpenCV are therefore demonstrated as additional face-isolation and quality-check steps; they are not necessarily applied as a preprocessing stage to every training image. A production pipeline should explicitly connect live-camera face detection, face-quality checks, classification, and alerting.

## 6. Model approach

### Why MobileNetV2?

Training a deep convolutional network from scratch on a relatively small image dataset can overfit and requires more data and compute. MobileNetV2 provides useful visual representations learned from ImageNet and is designed to be relatively efficient.

The notebook uses:

- MobileNetV2 with ImageNet pretrained weights.
- `include_top=False` to remove the original ImageNet classification head.
- A custom binary classification head.
- MobileNetV2 `preprocess_input`, which scales image values to the expected range.
- Binary cross-entropy loss.

### Two-phase training

**Phase 1 — Frozen base:** Keep the pretrained MobileNetV2 feature extractor frozen and train the newly added classification head. This allows the classifier to adapt without immediately changing the pretrained features.

**Phase 2 — Fine-tuning:** Unfreeze selected later layers and continue training with a much smaller learning rate. Batch Normalization layers are kept frozen in the notebook to support stable fine-tuning.

Callbacks include Early Stopping, ReduceLROnPlateau, and ModelCheckpoint.

## 7. Evaluation

The notebook reports:

- Accuracy
- Precision
- Drowsy-class recall
- F1-score
- Classification report
- Confusion matrix
- Training/validation accuracy and loss curves
- False-negative examples
- Precision/recall/F1 behaviour across decision thresholds

### Safety-focused interpretation

A false negative means an actually drowsy driver is classified as non-drowsy. This is the more safety-critical error in this use case. Drowsy-class recall should therefore receive particular attention, while precision must also be monitored to avoid excessive false alarms.

**Important validation caution:** In the current notebook, the threshold-analysis cell iterates over `y_true` and `y_prob` created from `test_ds`. Choosing a threshold based on test labels uses the test set for model selection and makes the final test result optimistic. For a clean evaluation, select the threshold using validation data only, freeze that threshold, and evaluate the test set once. Update the threshold-analysis cell accordingly before presenting the test score as an unbiased final result.

Do not report a metric value in this README unless it has been generated by a completed run and its evaluation split and decision threshold are clearly stated.

## 8. TensorFlow Lite and edge deployment

The notebook converts the trained Keras model into three TensorFlow Lite variants:

| Variant | Purpose / trade-off |
|---|---|
| Float32 | Baseline TFLite conversion; generally preserves floating-point behaviour |
| Float16 | Reduces weight storage; supported hardware may accelerate inference |
| INT8 | Uses integer quantization with representative data calibration; can reduce size and improve performance on supported hardware, with possible accuracy impact |

The notebook compares saved model sizes and demonstrates inference using the Float16 TFLite model.

For a deployment decision, compare each variant on the target device for:
- Model file size
- Inference latency and throughput
- Peak memory use
- Drowsy recall and false-negative count
- Output consistency against the original Keras model

The representative dataset and input preprocessing used during INT8 conversion must match the model's actual inference input pipeline.

## 9. Business questions

The notebook includes responses to the case-study questions:

1. Why transfer learning is preferable to training from scratch with limited data.
2. Why missing a drowsy driver is more dangerous than a false alarm, and why recall matters.
3. How augmentation and evaluation under different lighting conditions can improve robustness.
4. Why face isolation reduces irrelevant background information and what can go wrong when detection fails.
5. How MobileNetV2 and TFLite quantization support edge deployment, including accuracy/precision trade-offs.
6. Why frozen-base training followed by fine-tuning is a stable transfer-learning strategy.
7. Why accuracy alone is insufficient for a safety-critical classifier.
8. Practical improvements based on false-negative analysis and validation-based threshold tuning.

## 10. Technology stack

- Python
- TensorFlow / Keras
- MobileNetV2
- TensorFlow Lite
- OpenCV
- Dlib
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- Google Colab / Jupyter Notebook

## 11. Run the notebook

### Google Colab

1. Download or open the notebook in Google Colab.
2. Obtain the dataset from the link in the Dataset section.
3. Upload or extract the dataset using the notebook's optional download/extraction cells.
4. Confirm that `DATASET_DIR` points to the folder containing `train` and `test`.
5. Run the notebook cells in order, from top to bottom.
6. Review dataset counts, sample images, and face-detection results before training.
7. Complete both training phases.
8. Review training curves, classification metrics, confusion matrix, and false-negative examples.
9. Use validation data—not test labels—to select the operating threshold.
10. Run TFLite conversion, inference, and model-size comparison.
11. Download the generated model files or the ZIP archive using the final notebook cells.

### Local environment

Install the core dependencies in a compatible Python environment:

```bash
pip install tensorflow opencv-python dlib numpy pandas matplotlib seaborn scikit-learn
```

Dlib may require platform-specific build tools. If installation fails, use a compatible prebuilt package or run the notebook in an environment where Dlib is available. The notebook's face-detection sections require the relevant library.

TensorFlow, CUDA, and Python compatibility depends on the runtime platform. For reproducibility, record the Python and package versions used for the final run.

## 12. Generated model artifacts

After successful execution, the notebook is designed to create:

```text
drowsiness_model.keras
drowsiness_mobilenetv2_float32.tflite
drowsiness_mobilenetv2_float16.tflite
drowsiness_mobilenetv2_int8.tflite
drowsiness_models.zip
```

The ZIP contains the model files that exist at the time the download cell is run.

## 13. Limitations and next steps

- A still-image classifier does not, by itself, establish continuous driver drowsiness. A real system should analyse a sequence of frames and temporal cues.
- Performance may change with night-time lighting, shadows, glasses, masks, head pose, camera placement, motion blur, and different driver populations.
- Face-detection failures and low-quality crops need explicit handling; do not silently classify invalid frames.
- Dataset leakage can inflate performance. Where possible, split by driver and recording session.
- Thresholds must be selected on validation data and tested on an untouched test set.
- Quantized models must be benchmarked on the actual target hardware.
- A production system should use temporal smoothing, alert cooldowns, sensor/camera health monitoring, fail-safe behaviour, and human-factors testing.
- The prototype requires broader real-world validation and safety assessment before operational use.

## 14. Repository structure

A simple repository layout is:

```text
Driver-Drowsiness-Detection/
├── notebooks/
│   └── driver-drowsiness-mobilenetv2-complete-final.ipynb
├── models/                  # Optional: keep large model files out of Git
├── README.md
└── requirements.txt         # Optional: pin versions from the tested runtime
```

Do not commit the original dataset, private driver images, or large generated model files unless you have permission and a clear reason. Use Git LFS or a model-artifact store if large model files need to be versioned.

## 15. Dataset and reference documents

- **Dataset:** [Driver Drowsiness Detection Systems Dataset](https://drive.google.com/file/d/1Z8VTDfzAgz67j6u3FKBmdpWG16xiESJB/view?usp=sharing)
- **Dataset description / approach document:** [Google Docs reference](https://docs.google.com/document/d/1MEK9YrTqYObZFu4-b6a-1gsxafpRdxV__kZS15jaiFk/edit)

---

**Project:** Driver Drowsiness Detection System  
**Model:** MobileNetV2 Transfer Learning  
**Task:** Binary image classification — Drowsy / Non-Drowsy  
**Deployment format:** TensorFlow Lite
