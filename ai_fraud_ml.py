# ai_fraud_ml.py
import re
from joblib import load
from functools import lru_cache

@lru_cache(maxsize=1)
def _load():
    return load("fraud_model.joblib"), load("vectorizer.joblib")

def _amt_token(v):
    try:
        v = float(v)
        if v < 100: return "AMOUNT_BIN:LOW"
        if v < 1000: return "AMOUNT_BIN:MED"
        return "AMOUNT_BIN:HIGH"
    except Exception:
        return "AMOUNT_BIN:UNK"

def _combine(subject, body, from_domain, reply_domain, attachment_types, amount):
    txt = "\n".join([
        subject or "", body or "",
        f"FROM:{(from_domain or '').lower()}",
        f"REPLY:{(reply_domain or '').lower()}",
        f"ATTACH:{(attachment_types or '').lower()}",
        _amt_token(amount)
    ])
    return re.sub(r"\s+"," ", txt).strip()

def predict_email_risk(subject, body, from_domain, reply_domain, attachment_types, amount):
    clf, vec = _load()
    X = vec.transform([_combine(subject, body, from_domain, reply_domain, attachment_types, amount)])
    proba = float(clf.predict_proba(X)[0,1])
    risk_score = int(round(proba*100))

    # quick explain: top positive-weight tokens present
    try:
        feats = vec.get_feature_names_out()
        weights = clf.coef_[0]
        idx = X.nonzero()[1]
        toks = [(feats[i], weights[i]) for i in idx]
        toks.sort(key=lambda x: x[1], reverse=True)
        top_tokens = [t for t,w in toks[:5] if w>0][:5]
    except Exception:
        top_tokens = []

    return {"risk_score": risk_score, "top_tokens": top_tokens}
