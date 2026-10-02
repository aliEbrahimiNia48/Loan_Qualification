import tkinter as tk
from pathlib import Path
from tkinter import ttk

import joblib
import pandas as pd

# CONFIG
INPUT_WIDTH = 24
BG_COLOR = "#5a5a5a"
FG_COLOR = "white"
BTN_BG = "#e0e0e0"
FONT_TITLE = ("Helvetica", 16, "bold")
FONT_LABEL = ("Helvetica", 11)
FONT_RESULT = ("Helvetica", 13, "bold")

# LOAD MODELS
# Paths are relative to this file, so the app also works when started from another folder
BASE_DIR = Path(__file__).resolve().parent
try:
    model_lr = joblib.load(BASE_DIR / "model_1_LR.pkl")  # Logistic Regression
    model_rf = joblib.load(BASE_DIR / "model_2_RF.pkl")  # Random Forest
except Exception as e:
    raise RuntimeError(f"❌ Failed to load models: {e}")

# MAIN WINDOW
root = tk.Tk()
root.title("Loan Approval Decision Support System")
root.geometry("900x600")
root.configure(bg=BG_COLOR)

# MAIN FRAME (CENTERED)
main_frame = ttk.Frame(root)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

style = ttk.Style()
style.theme_use("default")

style.configure("TFrame", background=BG_COLOR)
style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=FONT_LABEL)
style.configure("TButton", background=BTN_BG, font=("Helvetica", 11, "bold"))
style.map("TButton", background=[("active", "#d0d0d0")])

# TITLE
title_label = ttk.Label(
    main_frame,
    text="Loan Application Input",
    font=FONT_TITLE
)
title_label.grid(row=0, column=0, columnspan=4, pady=(0, 25))

# INPUT FRAME
input_frame = ttk.Frame(main_frame)
input_frame.grid(row=1, column=0, columnspan=4)

# VARIABLES
vars_numeric = {
    "ApplicantIncome": tk.StringVar(value="5000"),
    "CoapplicantIncome": tk.StringVar(value="0"),
    "LoanAmount": tk.StringVar(value="120"),
    "Loan_Amount_Term": tk.StringVar(value="360"),
}

vars_categorical = {
    "Gender": tk.StringVar(value="Male"),
    "Married": tk.StringVar(value="No"),
    "Dependents": tk.StringVar(value="3+"),
    "Education": tk.StringVar(value="Not Graduate"),
    "Self_Employed": tk.StringVar(value="No"),
    "Property_Area": tk.StringVar(value="Urban"),
    "Credit_History": tk.StringVar(value="Bad (No Credit History)")
}

credit_map = {
    "Good (Has Credit History)": 1,
    "Bad (No Credit History)": 0
}

# Readable labels for the GUI (keys are the column names the models expect)
LABELS = {
    "ApplicantIncome": "Applicant Income",
    "CoapplicantIncome": "Coapplicant Income",
    "LoanAmount": "Loan Amount (thousands)",
    "Loan_Amount_Term": "Loan Term (months)",
    "Credit_History": "Credit History",
    "Gender": "Gender",
    "Married": "Married",
    "Dependents": "Dependents",
    "Education": "Education",
    "Self_Employed": "Self Employed",
    "Property_Area": "Property Area",
}


# FIELD BUILDER

def add_field(row, col, key, widget):
    ttk.Label(input_frame, text=LABELS[key]).grid(row=row, column=col, padx=10, pady=8, sticky="e")
    widget.grid(row=row, column=col + 1, padx=10, pady=8, sticky="w")


# LEFT COLUMN

row = 0
for key in ["ApplicantIncome", "LoanAmount", "Credit_History", "Married", "Education", "Property_Area"]:
    if key == "Credit_History":
        add_field(
            row, 0, key,
            ttk.Combobox(
                input_frame,
                textvariable=vars_categorical[key],
                values=list(credit_map.keys()),
                state="readonly",
                width=INPUT_WIDTH
            )
        )
    elif key in vars_numeric:
        add_field(
            row, 0, key,
            ttk.Entry(input_frame, textvariable=vars_numeric[key], width=INPUT_WIDTH)
        )
    else:
        add_field(
            row, 0, key,
            ttk.Combobox(
                input_frame,
                textvariable=vars_categorical[key],
                values=["Yes", "No"] if key in ["Married"] else
                ["Graduate", "Not Graduate"] if key == "Education" else
                ["Urban", "Semiurban", "Rural"],
                state="readonly",
                width=INPUT_WIDTH
            )
        )
    row += 1

# RIGHT COLUMN

row = 0
for key in ["CoapplicantIncome", "Loan_Amount_Term", "Gender", "Dependents", "Self_Employed"]:
    if key in vars_numeric:
        add_field(
            row, 2, key,
            ttk.Entry(input_frame, textvariable=vars_numeric[key], width=INPUT_WIDTH)
        )
    else:
        add_field(
            row, 2, key,
            ttk.Combobox(
                input_frame,
                textvariable=vars_categorical[key],
                values=["Male", "Female"] if key == "Gender" else
                ["0", "1", "2", "3+"] if key == "Dependents" else
                ["Yes", "No"],
                state="readonly",
                width=INPUT_WIDTH
            )
        )
    row += 1

# RESULT LABEL

result_label = ttk.Label(
    main_frame,
    text="",
    font=FONT_RESULT
)
result_label.configure(justify="center")
result_label.grid(row=2, column=0, columnspan=4, pady=25)


# PREDICTION FUNCTION

def read_numeric_inputs():
    """Return the numeric fields as floats, or raise ValueError with a message for the user."""
    values = {}
    for key, var in vars_numeric.items():
        text = var.get().strip().replace(",", "")
        try:
            value = float(text)
        except ValueError:
            raise ValueError(f"{LABELS[key]} must be a number")
        if value < 0:
            raise ValueError(f"{LABELS[key]} cannot be negative")
        values[key] = value

    if values["LoanAmount"] == 0 or values["Loan_Amount_Term"] == 0:
        raise ValueError("Loan Amount and Loan Term must be greater than 0")
    return values


def loan_decision(df):
    """Two-model decision: automatic only when both models agree, otherwise manual review."""
    pred_lr = model_lr.predict(df)[0]
    pred_rf = model_rf.predict(df)[0]
    prob_lr = model_lr.predict_proba(df)[0][1]
    prob_rf = model_rf.predict_proba(df)[0][1]

    if pred_lr == 1 and pred_rf == 1:
        decision = "APPROVED"
    elif pred_lr == 0 and pred_rf == 0:
        decision = "REJECTED"
    else:
        decision = "MANUAL REVIEW"
    return decision, prob_lr, prob_rf


RESULT_COLORS = {"APPROVED": "#00ff99", "REJECTED": "#ff6666", "MANUAL REVIEW": "#ffd966"}


def evaluate():
    try:
        data = {
            **read_numeric_inputs(),
            **{k: v.get() for k, v in vars_categorical.items()}
        }
    except ValueError as e:
        result_label.config(text=f"Invalid input: {e}", foreground="orange")
        return

    data["Credit_History"] = credit_map[data["Credit_History"]]

    try:
        decision, prob_lr, prob_rf = loan_decision(pd.DataFrame([data]))
    except Exception as e:
        result_label.config(text=f"Error: {e}", foreground="orange")
        return

    result_label.config(
        text=(f"Final Decision: {decision}\n"
              f"Approval probability — Logistic Regression: {prob_lr:.0%}, Random Forest: {prob_rf:.0%}"),
        foreground=RESULT_COLORS[decision]
    )


# BUTTON

btn = ttk.Button(
    main_frame,
    text="Evaluate Loan Application",
    command=evaluate
)
btn.grid(row=3, column=0, columnspan=4, pady=15)

# START

root.mainloop()
