# NCR Ride Completion Prediction Project

This project aims to predict the likelihood of ride completion in the National Capital Region (NCR) based on booking-time features.

## Project Structure

- `data/`: Placeholder for datasets (e.g., `NCR_Ride_Completion_Prediction (9).csv`).
- `notebooks/`: Original Jupyter notebooks.
- `src/`: Source code for the production pipeline.
  - `preprocessing.py`: Data cleaning and feature engineering.
  - `model.py`: Training, evaluation, and threshold optimization.
  - `utils.py`: Plotting and helper functions.
  - `predict.py`: Inference utilities.
- `models/`: Directory for saved model artifacts.
- `main.py`: Main orchestration script.
- `requirements.txt`: Python dependencies.

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the Model**:
   Execute the main script to process data, train models, and save the best one.
   ```bash
   python main.py
   ```

3. **Inference**:
   Use `src/predict.py` to load the saved model and perform predictions on new booking requests.

## Key Features

- **Leakage Prevention**: Only features available at booking time are used.
- **Cost-Sensitive Learning**: Thresholds are optimized based on the business costs of false positives (incorrectly predicting completion) and false negatives (missed completion opportunities).
- **Time-Based Validation**: Models are validated on data chronologically subsequent to training data.
- **Explainability**: Ready for SHAP analysis to understand feature drivers.
