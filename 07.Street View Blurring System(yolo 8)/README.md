# YouTube Shorts Performance Prediction

## 📌 Overview

This project uses **Supervised Machine Learning and Advanced Analytics** to predict the performance potential of YouTube Shorts.

The analysis focuses on understanding how video characteristics and publishing behavior influence engagement. The objective is to identify patterns associated with high-performing Shorts and provide data-driven recommendations that can help creators improve content reach and monetization.

---

## 🎯 Objectives

- Calculate and analyze YouTube Shorts Engagement Rate.
- Categorize Shorts into Low, Medium, and High performance groups.
- Investigate potential class imbalance in the target variable.
- Analyze the relationship between video duration and engagement.
- Identify effective upload time periods.
- Compare engagement across content categories.
- Analyze the impact of title characteristics.
- Build and compare supervised machine learning models.
- Identify the most important features driving performance prediction.
- Evaluate model performance using cross-validation and test-set metrics.
- Provide actionable recommendations for YouTube creators.

---

## 📂 Dataset

The dataset contains information related to YouTube Shorts, including:

- Video characteristics
- Video duration
- Content category
- Upload hour
- Title information
- Views and engagement-related metrics
- Other raw and derived video attributes

**Dataset:**  
https://www.kaggle.com/datasets/gangadharpanda/license-plate-detection-and-blurring

**Dataset Description:**  
https://docs.google.com/document/d/1Py4dq00Lvo9DqOkYHWg9RhXqwKI17R6u6NjoJy4nYVA/edit?usp=sharing

---

## 🔍 Business Questions

The analysis answers the following questions:

1. What is the Engagement Rate distribution, and does the target variable have class imbalance?
2. What relationship exists between video duration and Engagement Rate?
3. Is there an effective upload-hour range for achieving higher engagement?
4. Which content categories consistently achieve higher or lower engagement?
5. How do title length, word count, and question marks influence performance?
6. Which five features are most important to the best-performing model?
7. Which model performs best based on cross-validation and test-set F1-macro and ROC-AUC?
8. What practical actions can creators take to improve the probability of producing high-performing Shorts?

---

## 📊 Engagement Rate

The project calculates Engagement Rate to measure the level of audience interaction with each Short.

The resulting Engagement Rate is used to categorize videos into three performance groups:

```text
Low Performance
       │
       ▼
Medium Performance
       │
       ▼
High Performance
```

Tertile-based categorization is used to create the target variable for supervised classification.

---

## ⚙️ Feature Engineering

The analysis includes both raw and engineered features.

### Video Features

- `duration_sec`
- Views and engagement metrics
- Video/category characteristics

### Publishing Features

- `upload_hour`
- Publishing-time characteristics

### Title Features

- `titlelenchars`
- `titlewordcount`
- `titlehasquestion_mark`

These features are used to investigate how video structure, publishing behavior, and title characteristics influence performance.

---

## 🔬 Exploratory Data Analysis

The notebook analyzes:

- Engagement Rate distribution
- Target class distribution
- Engagement vs video duration
- Engagement by upload hour
- Engagement by content category
- Title length vs performance
- Title word count vs performance
- Question mark usage vs performance
- Feature correlations
- High-performing vs low-performing Shorts

Visualizations are used to identify patterns and relationships that may not be visible from summary statistics alone.

---

## 🤖 Machine Learning

The project uses supervised classification models to predict whether a Short belongs to a particular performance category.

The machine learning workflow includes:

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
Target Creation
     │
     ▼
Train / Test Split
     │
     ▼
Model Training
     │
     ▼
Cross-Validation
     │
     ▼
Model Comparison
     │
     ▼
Feature Importance
     │
     ▼
Business Recommendations
```

---

## 📈 Model Evaluation

Models are evaluated using classification metrics appropriate for multi-class performance prediction.

| Metric | Purpose |
|---|---|
| F1-Macro | Measures performance across all classes while giving each class equal importance |
| ROC-AUC | Measures the model's ability to distinguish between performance classes |
| Cross-Validation | Evaluates model stability across different training/validation splits |
| Test Performance | Measures generalization on unseen data |

The final model is selected based on a combination of validation performance, test-set performance, and suitability for deployment.

---

## 🔎 Feature Importance & Model Explainability

Feature importance is analyzed to identify the variables that contribute most strongly to performance prediction.

The analysis specifically examines:

- Video duration
- Upload hour
- Content category
- Title length
- Title word count
- Title question-mark indicator
- Other raw and engineered features

The top five features from the best-performing model are interpreted from a business perspective to understand why they may influence Shorts performance.

> Feature importance indicates predictive association and should not automatically be interpreted as proof of causal impact.

---

## 💡 Business Insights

The project focuses on identifying:

### Optimal Video Duration

Determine whether a particular duration range is associated with a higher probability of achieving High performance.

### Publishing Time

Identify upload-hour patterns associated with higher average Engagement Rate.

### Content Category

Identify categories that consistently outperform or underperform and use these findings to inform content planning.

### Title Strategy

Understand how title length, word count, and question-based titles relate to performance.

### Predictive Drivers

Identify the strongest features used by the final model to predict Shorts performance.

---

## 🚀 Actionable Recommendations

The final recommendations are based on the combined results of:

- Exploratory Data Analysis
- Feature engineering
- Model performance
- Feature importance
- Model explainability

Potential recommendation areas include:

1. Optimize video duration based on the observed high-engagement range.
2. Prioritize upload time slots associated with stronger Engagement Rates.
3. Focus content planning on categories with consistently stronger engagement.
4. Optimize title structure using the observed relationship between title characteristics and performance.
5. Use the most predictive features as data-driven inputs for future content planning and experimentation.

---

## 📓 Notebook

The complete analysis is available in the **Google Colab notebook**.

The notebook contains:

- Data loading
- Data cleaning
- Engagement Rate calculation
- Target creation
- Exploratory Data Analysis
- Feature engineering
- Visualization
- Model training
- Cross-validation
- Model comparison
- Test-set evaluation
- Feature importance
- Business insights
- Final recommendations

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Google Colab
- Jupyter Notebook

---

## 📁 Project Structure

```text
YouTube-Shorts-Performance-Prediction/
│
├── README.md
└── YouTube_Shorts_Performance_Prediction.ipynb
```

> The dataset is not included in this repository unless permitted by the dataset license.

---

## 🚀 How to Run

1. Clone the repository.
2. Open the `.ipynb` notebook in Google Colab or Jupyter Notebook.
3. Download the dataset from the provided source.
4. Upload the dataset to the notebook environment.
5. Update the dataset path if required.
6. Run the notebook cells sequentially.

---

## 📌 Expected Outcome

The project aims to deliver:

- A classification model for YouTube Shorts performance.
- Understanding of factors associated with high Engagement Rate.
- Identification of effective publishing time periods.
- Identification of high-performing content categories.
- Analysis of title characteristics.
- A ranked set of important predictive features.
- Data-driven recommendations for improving Shorts performance.

---

## 👤 Author

**Gangadhar Panda**

---

## 📌 Conclusion

This case study demonstrates how supervised machine learning and advanced analytics can be used to understand and predict YouTube Shorts performance.

By combining engagement analysis, feature engineering, exploratory visualization, machine learning, model explainability, and business interpretation, the project provides a data-driven framework that creators can use to improve content strategy, publishing decisions, audience engagement, and potential monetization.
