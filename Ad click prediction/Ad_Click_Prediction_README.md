# Ad Click Prediction (CTR) Case Study

## 📌 Overview

In digital advertising, predicting whether a user will click an advertisement is critical for optimizing ad spend, improving targeting, and delivering more relevant advertisements.

This project focuses on building a **Click-Through Rate (CTR) prediction model** using user, product, campaign, device, and contextual information.

The dataset contains a highly imbalanced target variable because ad clicks are relatively rare compared with ad impressions. The project therefore focuses on effective feature engineering, imbalance handling, model training, and business-oriented evaluation.

---

## 🎯 Objectives

- Understand user, product, campaign, and ad interaction data.
- Analyze factors influencing ad clicks.
- Perform data cleaning and preprocessing.
- Create behavioral, temporal, and contextual features.
- Handle the highly imbalanced click/no-click target.
- Compare suitable binary classification models.
- Evaluate models using business-relevant metrics.
- Identify important features driving ad clicks.
- Answer key business questions related to CTR.
- Generate actionable recommendations for ad targeting and bidding.

---

## 📂 Dataset

The dataset contains information related to:

- User interactions
- Product information
- Ad campaigns
- Device/context information
- User demographics
- Webpage information
- Ad click behavior

The target variable represents whether an advertisement was clicked.

> **Note:** The dataset is not included in this repository unless permitted by the dataset license.

---

## 🔍 Business Questions

The analysis addresses the following questions:

1. Do weekend users click more than weekday users?
2. Which products generate the highest CTR and which perform poorly?
3. Do personalized features such as user-product interactions improve CTR prediction?
4. Which factors, such as webpage information or user sessions, drive clicks the most?
5. How effective is SMOTE in reducing false negatives for rare click events?
6. Can aggregated product CTR features help forecast inventory needs for high-performing advertisements?
7. Which user profiles show higher click propensity, and how can this support bidding strategies?

---

## 🧹 Data Preparation

The preprocessing pipeline includes:

- Dataset shape and structure analysis
- Data type validation
- Missing value analysis
- Duplicate record checks
- Missing value imputation
- Numerical feature processing
- Categorical feature encoding
- Target variable analysis
- Outlier and data-quality checks

---

## ⚙️ Feature Engineering

Several feature groups are considered to improve CTR prediction.

### Temporal Features

Examples include:

- Hour
- Day of week
- Month
- Weekend indicator

### Behavioral Features

Examples include:

- User interaction patterns
- User session information
- Historical click behavior
- User-product interactions

### Product Features

Examples include:

- Product category
- Product-level CTR
- Product interaction frequency
- Historical product performance

### Contextual Features

Examples include:

- Webpage information
- Device information
- Campaign information
- User demographic information
- City/development indicators

---

## ⚖️ Handling Class Imbalance

Ad clicks are relatively rare compared with non-click events, creating a highly imbalanced classification problem.

The project evaluates techniques such as:

- SMOTE
- Class weighting
- Stratified train/test splitting

The impact of imbalance handling is evaluated based on model performance, particularly its ability to identify positive click events without creating excessive false positives.

---

## 🤖 Machine Learning Models

The project evaluates binary classification algorithms suitable for CTR prediction.

Potential models include:

- Logistic Regression
- Random Forest
- LightGBM

Hyperparameter optimization and validation techniques are used where appropriate.

---

## 📊 Model Evaluation

Model performance is evaluated using metrics suitable for imbalanced classification.

| Metric | Purpose |
|---|---|
| ROC-AUC | Measures the model's ability to distinguish clicks from non-clicks across classification thresholds |
| F1-Score | Balances precision and recall |
| Precision | Measures how many predicted clicks are actual clicks |
| Recall | Measures how many actual clicks are successfully identified |
| Confusion Matrix | Shows true/false positives and negatives |

The final model selection considers both predictive performance and real-world ad-serving requirements.

---

## 📈 Exploratory Data Analysis

The notebook includes visual analysis such as:

- Click vs non-click distribution
- CTR by product
- CTR by weekday/weekend
- CTR by hour
- CTR by user demographics
- CTR by device/context
- Product-level click performance
- Correlation analysis
- Feature importance

These visualizations help identify patterns that may not be obvious from summary statistics alone.

---

## 🔬 Feature Importance & Interpretability

Feature importance is analyzed to identify the variables that contribute most to click prediction.

The analysis focuses on factors such as:

- Webpage ID
- User session behavior
- Product information
- User-product interaction
- Device/context
- Temporal behavior
- User demographics

The results are used to identify opportunities for better targeting and ad placement.

---

## 💼 Business Insights

The analysis is designed to support several practical business decisions:

### Ad Targeting

Identify user segments and contexts with higher click propensity.

### Bidding Strategy

Use predicted click probability to prioritize valuable impressions and adjust bidding strategies.

### Product Optimization

Identify products with consistently high or low CTR and optimize campaign allocation accordingly.

### Inventory Forecasting

Use historical product CTR and interaction trends to estimate demand for high-performing advertisements.

### User Experience

Improve ad relevance by reducing unnecessary impressions and targeting users with more relevant advertisements.

---

## 🧪 SMOTE Analysis

SMOTE is evaluated to understand whether synthetic minority samples improve detection of rare click events.

The analysis compares model performance before and after imbalance handling, focusing on:

- Recall
- F1-Score
- ROC-AUC
- False negatives
- False positives
- Training data size
- Potential production implications

A key consideration is that SMOTE is primarily a **training-time technique**. Synthetic samples do not need to be generated during real-time ad serving.

---

## 🚀 Machine Learning Pipeline

```text
Raw Dataset
     │
     ▼
Data Understanding
     │
     ▼
Data Cleaning
     │
     ▼
Feature Engineering
     │
     ▼
Categorical Encoding
     │
     ▼
Train/Test Split
     │
     ▼
Class Imbalance Handling
     │
     ▼
Model Training
     │
     ▼
Hyperparameter Tuning
     │
     ▼
Model Evaluation
     │
     ▼
Feature Importance
     │
     ▼
Business Insights
```

---

## 📓 Notebook

The complete implementation is available in the Google Colab/Jupyter notebook.

The notebook contains:

- Data loading
- Data exploration
- Data cleaning
- Feature engineering
- Visualization
- Imbalance handling
- Model training
- Model comparison
- Evaluation
- Feature importance
- Business recommendations

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- LightGBM
- Imbalanced-learn
- Google Colab
- Jupyter Notebook

---

## 📁 Project Structure

```text
Ad-Click-Prediction/
│
├── README.md
└── Ad_Click_Prediction.ipynb
```

> The dataset is not included in the repository unless permitted by the dataset license.

---

## 🚀 How to Run

1. Clone the repository.
2. Open the `.ipynb` notebook in Google Colab or Jupyter Notebook.
3. Download the required dataset from the provided dataset source.
4. Upload the dataset to the notebook environment.
5. Update the dataset path if required.
6. Run the notebook cells sequentially.

---

## 📌 Expected Outcome

The project aims to produce a predictive CTR model that can:

- Estimate the probability of an ad click.
- Identify high-value user and product segments.
- Understand the major drivers of clicks.
- Support data-driven bidding and targeting.
- Help improve advertising efficiency.
- Reduce irrelevant ad impressions.

---

## 👤 Author

**Gangadhar Panda**

---

## 📌 Conclusion

This case study demonstrates how machine learning can be applied to digital advertising to predict user click behavior.

By combining data preprocessing, behavioral and contextual feature engineering, imbalance handling, classification models, and feature importance analysis, the project provides a data-driven approach for improving ad targeting, bidding strategies, inventory planning, and user experience.
