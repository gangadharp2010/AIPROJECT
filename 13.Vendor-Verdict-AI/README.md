# Vendor Verdict – Can We Trust This AI Tool?

An evidence-based AI vendor risk assessment solution that evaluates security, privacy, and data protection requirements using vendor-specific evidence.

## 1. Project Overview

Organizations increasingly rely on third-party AI tools to process business and customer data. Before adopting these tools, organizations must assess whether vendors satisfy security, privacy, compliance, and data governance requirements.

**Vendor Verdict** aims to automate this assessment by analyzing available vendor evidence and assigning compliance verdicts to individual requirements.

The solution follows an evidence-first approach: unsupported claims are not automatically treated as verified compliance, and missing evidence is handled conservatively.

## 2. Problem Statement

Evaluating AI vendors manually is time-consuming and requires reviewing multiple sources, including:

- Official vendor documentation
- Security and compliance pages
- Privacy policies
- Data processing agreements
- Subprocessor disclosures
- Security incident reports
- Data retention and residency policies

The objective is to build a repeatable assessment pipeline that extracts relevant facts, evaluates requirements, and generates an overall vendor decision.

## 3. Key Features

- Vendor-specific evidence analysis
- Official-domain validation
- Trusted-source filtering
- Date-aware evidence selection
- Security and privacy fact extraction
- Prompt-injection-aware evidence handling
- Rule-based requirement assessment
- Conservative UNKNOWN and NEEDS_REVIEW classification
- Overall vendor approval decisions
- Holdout validation and Kaggle submission generation

## 4. Solution Architecture

The solution follows a modular evidence-processing workflow.

```text
Competition Dataset
        |
        v
Data Loading and Validation
        |
        v
Vendor and Case Identification
        |
        v
Evidence Source Filtering
        |
        v
Official Domain Validation
        |
        v
Evidence Extraction
        |
        v
Fact Mapping
        |
        v
Requirement Evaluation
        |
        v
Individual Verdicts
        |
        v
Overall Vendor Decision
        |
        v
Submission Generation
```

## 5. Evidence Extraction

The extraction pipeline evaluates the following vendor facts:

| Evidence Field | Description |
|---|---|
| security_certifications | Security certifications |
| data_regions | Data hosting and residency |
| trains_on_customer_data | Use of customer data for model training |
| subprocessors | Third-party subprocessors |
| data_retention | Data retention and deletion policies |
| sso_saml | SSO and SAML support |
| security_incidents | Security incident information |
| dpa_available | Data Processing Agreement availability |

Evidence is evaluated with attention to source reliability, vendor identity, official domain, and relevant dates.

Missing or insufficient evidence is not automatically interpreted as a negative compliance finding.

## 6. Verdict Classification

### Requirement-Level Verdicts

| Verdict | Meaning |
|---|---|
| PASS | Requirement is supported by sufficient evidence |
| FAIL | Evidence establishes that the requirement is not satisfied |
| UNKNOWN | Available evidence is insufficient to determine compliance |
| NEEDS_REVIEW | Additional verification or manual assessment is required |

### Overall Vendor Verdicts

| Verdict | Meaning |
|---|---|
| BLOCKED | At least one applicable requirement fails |
| CONDITIONAL | Evidence is missing or requires further review |
| READY_FOR_APPROVAL | All applicable requirements pass |

## 7. Dataset Information

The competition dataset used during development contains:

| Dataset | Records |
|---|---:|
| Vendor cases | 700 |
| Evidence pages | 7,396 |
| Training labels | 3,185 |
| Official evidence records | 5,020 |
| Test submission rows | 2,378 |

The dataset includes vendor metadata, evidence pages, requirement definitions, training labels, and test records.

**Note:** Competition input data is not included in this repository. Users must obtain the dataset through the official Kaggle competition.

## 8. Evaluation Methodology

The solution uses a local holdout validation process and multiple random seeds to assess prediction stability.

The official competition metric combines:

- Requirement-level macro F1: 60%
- Overall decision accuracy: 20%
- False-confidence reduction: 20%

The false-confidence component penalizes PASS or FAIL predictions when the actual verdict is UNKNOWN or NEEDS_REVIEW.

### Experimental Results

| Metric | Result |
|---|---:|
| Holdout score (seed 42) | 0.976017 |
| Five-seed average | 0.972783 |
| Five-seed standard deviation | 0.005970 |
| Public leaderboard score | 0.80014 |

*These are experimental results from different evaluation settings. Local holdout performance should not be interpreted as hidden-test performance.*

## 9. Technology Stack

- Python
- Pandas
- NumPy
- Regular Expressions
- Scikit-learn
- Jupyter Notebook
- Google Colab
- Kaggle

## 10. Repository Structure

```text
Vendor-Verdict-AI/
│
├── notebooks/
│   └── vendor-solution.ipynb
│
├── src/
│   ├── vendor_verdict.py
│   ├── evidence_extractor.py
│   ├── verdict_engine.py
│   └── evaluation.py
│
├── configs/
│   └── config.example.json
│
├── outputs/
│
├── requirements.txt
├── .gitignore
└── README.md
```

*The structure above is the recommended organization for the project. Include only files that exist in your repository.*

## 11. Installation and Execution

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

### Step 2: Navigate to the project

```bash
cd YOUR_REPOSITORY/Vendor-Verdict-AI
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Obtain the competition dataset

Visit the official competition:

https://www.kaggle.com/competitions/vendor-verdict-can-we-trust-this-ai-tool

Download or attach the competition dataset to your Kaggle notebook.

### Step 5: Run the notebook

Open `notebooks/vendor-solution.ipynb` in Kaggle or Google Colab with the required dataset available.

Execute the notebook cells sequentially to perform evidence extraction, requirement evaluation, validation, and submission generation.

## 12. Kaggle Submission

The solution generates a submission CSV containing:

- `id`
- `verdict`

The submission contains requirement-level and overall vendor predictions in the format required by the competition.

Validate the output against the competition sample submission before uploading it.

## 13. Important Design Principles

1. Evidence before conclusions.
2. Official-domain and vendor identity validation.
3. Date-aware evidence assessment.
4. No unsupported compliance assumptions.
5. Missing evidence must remain distinguishable from verified failure.
6. Untrusted evidence must not override assessment instructions.
7. Conservative verdict classification to reduce false confidence.

## 14. Future Improvements

- Improve evidence extraction using NLP and LLM-based information extraction.
- Introduce semantic evidence retrieval.
- Improve entity resolution and official-domain verification.
- Add evidence provenance and explainability.
- Expand test coverage for negation and plan-specific restrictions.
- Develop a vendor risk assessment dashboard.
- Explore RAG-based evidence-grounded compliance evaluation.

## 15. Disclaimer

This project was developed for the Kaggle competition **Vendor Verdict – Can We Trust This AI Tool**.

The generated assessments are automated predictions based on available competition evidence and defined evaluation rules. They should not replace professional security, legal, privacy, or compliance reviews.

## 16. Author

Developed as an AI/ML engineering project focused on evidence-based vendor risk assessment, information extraction, and trustworthy AI evaluation.

**Project:** Vendor Verdict – Can We Trust This AI Tool  
**Platform:** Kaggle  
**Language:** Python
