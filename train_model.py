# train_model.py
import pandas as pd, numpy as np, re
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump

CSV_PATH = "labeled_invoices.csv"

def amt_token(val):
    try:
        v = float(val)
        if v < 100: return "AMOUNT_BIN:LOW"
        if v < 1000: return "AMOUNT_BIN:MED"
        return "AMOUNT_BIN:HIGH"
    except Exception:
        return "AMOUNT_BIN:UNK"

def combine(row):
    subject = str(row.get("subject","") or "")
    body = str(row.get("body","") or "")
    from_dom = str(row.get("from_domain","") or "")
    reply_dom = str(row.get("reply_domain","") or "")
    attach = str(row.get("attachment_types","") or "")
    amt = row.get("amount","")
    txt = "\n".join([subject, body, f"FROM:{from_dom}", f"REPLY:{reply_dom}",
                     f"ATTACH:{attach}", amt_token(amt)])
    return re.sub(r"\s+"," ", txt).strip()

def main():
    df = pd.read_csv(CSV_PATH)
    for c in ["subject","body","from_domain","reply_domain","attachment_types"]:
        if c not in df.columns: df[c] = ""
        df[c] = df[c].fillna("")
    if "amount" not in df.columns: df["amount"] = np.nan
    if "label" not in df.columns: raise ValueError("Need 'label' column (0/1).")

    df["combined_text"] = df.apply(combine, axis=1)
    X = df["combined_text"].values
    y = df["label"].astype(int).values

    Xtr, Xva, ytr, yva = train_test_split(
        X, y, test_size=0.25, random_state=42,
        stratify=y if len(np.unique(y))>1 else None
    )

    vec = TfidfVectorizer(max_features=20000, ngram_range=(1,2), lowercase=True)
    Xtrv = vec.fit_transform(Xtr)
    Xvav = vec.transform(Xva)

    clf = LogisticRegression(max_iter=200, class_weight="balanced")
    clf.fit(Xtrv, ytr)

    print("\n=== Validation Report ===")
    print(classification_report(yva, clf.predict(Xvav), digits=3))

    dump(clf, "fraud_model.joblib")
    dump(vec, "vectorizer.joblib")
    print("\nSaved fraud_model.joblib and vectorizer.joblib")

if __name__ == "__main__":
    main()
