# Predicting Sales from Influencer Campaign Data

## Project overview

Marketing teams invest in influencer campaigns but need a better way to understand which campaign characteristics relate to product sales. This project focuses on predicting the number of product units sold from historical influencer-campaign attributes.

The project notes describe a deliberately messy dataset containing inconsistent formats, missing values, outliers, and mixed measurement scales—conditions that require careful data preparation before modeling.

## Problem statement

Build a regression workflow that estimates campaign sales using available attributes such as:

- Influencer follower count
- Engagement rate
- Campaign advertising spend (GBP)
- Content quality score
- Campaign end timestamp
- Sales units (target)

The exact columns and definitions should be confirmed against the dataset and approach document.

## Objectives

- Inspect the training and test data and document quality issues.
- Normalize numeric fields such as follower counts, engagement rates, and currency values.
- Handle missing values, inconsistent formats, impossible values, and outliers transparently.
- Explore relationships between campaign features and sales.
- Engineer useful features without leaking target information.
- Train and tune regression models using cross-validation.
- Evaluate predictions with RMSE and R² (and other appropriate regression metrics).
- Interpret important sales drivers and build a reusable prediction pipeline for future campaign records.

## Workflow

```text
Raw Campaign Data
       |
       v
Schema and Data-Quality Checks
       |
       v
Cleaning and Type Normalization
       |
       v
Exploratory Data Analysis
       |
       v
Feature Engineering
       |
       v
Train / Validation Strategy
       |
       v
Regression Model Training
       |
       v
Cross-Validation and Tuning
       |
       v
Test Evaluation
       |
       v
Feature Interpretation and Sales Insights
```

## Repository artifacts

- `document.md` — problem statement and dataset overview.
- `Approach document _ Predicting sales from campaign data.pdf` — methodology.
- `Predicting_Sales_Influencer_Campaigns_Final_Colab.ipynb` — Colab notebook.
- `Predicting_Sales_Influencer_Campaigns_Gangadhar_panda_latest.ipynb` — later notebook version.
- `Predicting_Sales_Influencer_Campaigns_Gangadhar_panda_latest.html` — notebook HTML export.
- `Predicting_Sales_Influencer_Campaigns_Gangadhar_panda_final.pdf` — final report.

The dataset is referenced in the project notes as a separate Google Drive resource. It is not currently listed as a CSV file in this project folder.

## Run the notebook

1. Open the latest notebook in Google Colab or Jupyter.
2. Obtain the campaign training/test data from the dataset location described in `document.md`.
3. Upload or mount the data and update notebook paths.
4. Review and install the dependencies required by the notebook.
5. Run the cells sequentially and inspect the data-quality, modeling, and evaluation outputs.

## Evaluation

Use a validation strategy that avoids using the test data during model selection. Report at least:

| Metric | Purpose |
|---|---|
| RMSE | Penalizes larger sales prediction errors and expresses error in the target's units |
| MAE | Average absolute difference between predicted and actual sales |
| R² | Measures the proportion of target variance explained by the model |

Compare any proposed model against a simple baseline. Investigate large residuals and ensure that timestamps or campaign fields unavailable at prediction time are not used as features.

## Business interpretation and limitations

Model feature importance can identify associations in the historical campaign data, but it cannot establish that increasing an influencer's followers, engagement, or ad spend will cause sales to increase. Campaign selection, budget allocation, and creative decisions should be tested with controlled experiments where feasible. Predictions should be used as decision support rather than a guarantee of campaign sales.

## Author

Gangadhar Panda
