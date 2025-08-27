# 📧 Email Invoice Bot

This project connects to Gmail via IMAP, scans your inbox for invoice-related emails, and saves the results into an Excel file called **`invoices.xlsx`**.

---

## 📋 Requirements

- Python **3.10 or newer**  
- Gmail account with **App Passwords** enabled  

### 🔑 How to set up a Gmail App Password
1. Go to **Google Account → Security**  
2. Enable **2-Step Verification**  
3. Generate an **App Password** for "Mail"  
4. Copy the **16-character password** (this replaces your normal Gmail password when using the bot)  

---

## ⚙️ Installation

Clone the repo and install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

---

## 🚀 Usage

Run the bot with:
```bash
python main.py
```


You will be prompted for:

- Your Gmail address  
- Your Gmail App Password (16 characters, hidden while typing)  
 
---

## 📂 Output

- The results are saved in **`invoices.xlsx`** inside your project folder  
- Each row in the file corresponds to an invoice email found  

The Excel file includes:

- Date → when the email was received
- Sender → who sent the invoice
- Subject → subject line of the email
- HasPDF → whether a PDF invoice was attached
- AmountGuess → first number detected in the body
- ML Risk Score → model’s risk estimate (0–100)
- ML Top Tokens → top keywords influencing the score

---

## 📝 Notes

- Your Gmail App Password will **not** be stored; it’s only used for the active session  
- By default, the bot scans the **newest 50 emails** to keep things fast  
- You can change this limit in the code if you want to scan more  
- Works with any Gmail account that has **IMAP** and **App Passwords** enabled 

---

## 🤖 Machine Learning Risk Scoring

In addition to extracting invoice emails into `invoices.xlsx`, this bot now includes a **fraud risk scoring step** powered by a simple Machine Learning model (`ai_fraud_ml.py`).

### What it does
- Every email that looks like an invoice is passed to the ML model.
- The model outputs:
  - **ML Risk Score** → a number between 0–100 (higher = more suspicious).
  - **ML Top Tokens** → the most important keywords that influenced the score.

### Example output

| From          | Subject     | HasPDF | AmountGuess | ML Risk Score | ML Top Tokens                  |
|---------------|-------------|--------|-------------|----------------|--------------------------------|
| Rayan Beidas  | Invoice #1  | TRUE   | 1234        | 50             | amount, gmail, high, pdf       |
| Google        | Security... | FALSE  | 35          | 47             | gmail, now                     |
| Talabat       | Your order  | FALSE  | 1           | 47             | vendor, payment, please, via   |

### Notes
- Current model is a demo — scores will cluster around ~45–55.
- For real use, you can retrain the model with your own data via `train_model.py` and `labeled_invoices.csv`.
- The ML columns are saved automatically into `invoices.xlsx`:
  - `ML Risk Score`
  - `ML Top Tokens`


