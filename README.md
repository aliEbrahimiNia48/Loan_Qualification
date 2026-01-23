# Loan Approval Decision Support System

A desktop-based Machine Learning application for evaluating loan applications using a trained classification model, with a clean and responsive Tkinter-based user interface.

---

## Project Overview

This project is a decision support system that predicts whether a loan application should be **Approved** or **Rejected** based on applicant financial and demographic information.  
It combines a trained machine learning model with a carefully designed desktop GUI to provide an intuitive, user-friendly experience.

---

## Features

- Machine Learning-based loan approval prediction (Logistic Regression)
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
3. The trained ML model processes the input data.
4. The system outputs a final decision:
   - **APPROVED** (green)
   - **REJECTED** (red)

---

## sHow to Run

1. Ensure Python 3 is installed.
2. Install required dependencies:
   ```bash
   pip install pandas scikit-learn joblib
