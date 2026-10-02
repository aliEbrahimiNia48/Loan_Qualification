# Loan Approval Decision Support System

A desktop-based Machine Learning application for evaluating loan applications using a trained classification model, with a clean and responsive Tkinter-based user interface.

---

## Project Overview

This project is a decision support system that predicts whether a loan application should be **Approved** or **Rejected** based on applicant financial and demographic information.  
It combines a trained machine learning model with a carefully designed desktop GUI to provide an intuitive, user-friendly experience.

---

## Features

- Two-model decision system (Logistic Regression + Random Forest):
  - both models approve → **APPROVED**
  - both models reject → **REJECTED**
  - the models disagree → **MANUAL REVIEW** by a human expert
- Approval probability of each model shown in the GUI
- Input validation (non-numeric, negative or zero values are rejected with a clear message)
- Clean, centered, desktop-optimized GUI using Tkinter
- Consistent and aligned input fields for professional UI appearance
- Controlled categorical inputs to prevent invalid user entries
- Real-time prediction result display with visual feedback (Approved / Rejected)

---

## Input Parameters

The system takes the following inputs:

- Applicant Income
- Coapplicant Income
- Loan Amount
- Loan Amount Term
- Credit History (Good / Bad)
- Gender
- Marital Status
- Number of Dependents
- Education Level
- Self Employed Status
- Property Area

---

## Technologies Used

- **Python 3**
- **scikit-learn** (model training & inference)
- **pandas** (data preprocessing)
- **joblib** (model persistence)
- **Tkinter & ttk** (desktop GUI)

---

## How It Works

1. User enters loan applicant information through the GUI.
2. Inputs are converted into a structured pandas DataFrame.
3. Both trained models (Logistic Regression and Random Forest) process the input data.
4. The system outputs a final decision:
   - **APPROVED** (green) – both models approve
   - **REJECTED** (red) – both models reject
   - **MANUAL REVIEW** (yellow) – the models disagree

---

## Project Files

| File | Description |
|------|-------------|
| `Final_3.ipynb` | Data analysis, preprocessing, model training (GridSearchCV), evaluation and model export |
| `loan.csv` | Dataset (614 loan applications) |
| `model_1_LR.pkl` | Trained Logistic Regression pipeline |
| `model_2_RF.pkl` | Trained Random Forest pipeline |
| `app.py` | Tkinter desktop application |

---

## Model Performance (test set, 123 applications)

| Model | CV F1 | Accuracy | F1 | ROC AUC | Rejection Recall |
|-------|-------|----------|----|---------|------------------|
| Logistic Regression | 0.871 | 0.862 | 0.908 | 0.852 | 0.579 |
| Random Forest | 0.870 | 0.854 | 0.903 | 0.809 | 0.553 |
| MLP | 0.868 | 0.846 | 0.898 | 0.813 | 0.526 |
| KNN | 0.868 | 0.837 | 0.891 | 0.833 | 0.553 |
| Baseline (approve everyone) | – | 0.691 | 0.817 | 0.500 | 0.000 |

Models are selected by cross-validation F1 on the training data, not by their test score.
*Rejection Recall* is the share of applications that should be rejected which the model also rejects; about 40% of
risky applications are still approved, which is why disagreements between the two models are sent to manual review.

---

## Limitations

- The dataset is small (614 rows), so the scores above can vary noticeably with a different train/test split.
- `Gender` and `Married` are used as model inputs. Using such attributes for credit decisions is not allowed in many
  countries; this project is for educational purposes and is not meant for real lending decisions.

---

## How to Run

1. Ensure Python 3 is installed.
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the application:
   ```bash
   python app.py
   ```
4. (Optional) Retrain the models by running all cells of `Final_3.ipynb`.
