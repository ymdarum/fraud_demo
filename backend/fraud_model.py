"""
fraud_model.py

This script reads `dataset.csv`, engineers a few simple risk features,
trains an anomaly detection model (Isolation Forest), and writes `dataset_scored.csv`.

Why Isolation Forest?
- It's a simple unsupervised anomaly detector.
- It works well for "rare weird patterns" demos.
- It produces an anomaly score you can convert to an easy 0→1 risk score.

Output columns (added):
- payment_ratio: amount / balance
- unusual_hour: 1 if payment is outside typical business hours
- high_risk_country: 1 if payment is in a higher-risk corridor list
- anomaly_score: model score (higher is "more normal" in sklearn's decision_function)
- fraud_flag: 1 for normal, -1 for anomaly
- risk_score: 0→1 (higher means riskier)

How to run:
  python backend/fraud_model.py
"""

from __future__ import annotations

import random

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Feature engineering.

    We keep features simple and explainable:
    - payment_ratio: big payment vs available balance can be liquidity-risky
    - unusual_hour: odd hours can indicate non-standard / automated / rushed actions
    - high_risk_country: simple corridor risk proxy for demo purposes
    """

    df = df.copy()

    # Avoid division by zero. In our generator balance should never be 0,
    # but we keep this guard to make the code safer and beginner-friendly.
    df["payment_ratio"] = df["amount"] / df["balance"].replace({0: np.nan})
    df["payment_ratio"] = df["payment_ratio"].fillna(0.0)

    # NOTE: We deliberately use the rule from the prompt:
    # unusual if < 8 or > 18. This makes the injected fraud (1-4 AM) stand out.
    df["unusual_hour"] = df["hour"].apply(lambda x: 1 if x < 8 or x > 18 else 0)

    high_risk = {"HK", "CN"}
    df["high_risk_country"] = df["country"].apply(lambda x: 1 if x in high_risk else 0)

    return df


def train_and_score(df: pd.DataFrame, contamination: float = 0.03, seed: int = 42) -> pd.DataFrame:
    """
    Train Isolation Forest and score each transaction.

    contamination:
      Rough expectation of anomaly fraction in the dataset.
      For demos, 0.03 is a nice small number.
    """

    df = df.copy()

    features = df[["amount", "payment_ratio", "unusual_hour", "high_risk_country"]]

    # Reproducibility helps when demoing to stakeholders.
    random.seed(seed)
    model = IsolationForest(contamination=contamination, random_state=seed)
    model.fit(features)

    # decision_function: higher means "more normal".
    df["anomaly_score"] = model.decision_function(features)
    df["fraud_flag"] = model.predict(features)

    # Convert anomaly_score into a 0→1 risk score:
    # - risk_score near 1 => very suspicious
    # - risk_score near 0 => looks normal
    score_max = df["anomaly_score"].max()
    score_min = df["anomaly_score"].min()
    denom = score_max - score_min

    # Avoid divide-by-zero if all scores are identical (unlikely, but safe).
    if denom == 0:
        df["risk_score"] = 0.0
    else:
        df["risk_score"] = (score_max - df["anomaly_score"]) / denom

    return df


def main() -> None:
    input_csv = "dataset.csv"
    output_csv = "dataset_scored.csv"

    df = pd.read_csv(input_csv)
    df = add_features(df)
    df = train_and_score(df)

    # Sort by most risky first. This makes the CSV and dashboard immediately impressive.
    df = df.sort_values("risk_score", ascending=False).reset_index(drop=True)

    df.to_csv(output_csv, index=False)
    print(f"Scored dataset written: {output_csv} (rows={len(df)})")

    # Print a tiny "stakeholder friendly" preview.
    preview = df[["txn_id", "company", "amount", "country", "hour", "risk_score", "fraud_flag"]].head(5)
    print("\nTop risky transactions (preview):")
    print(preview.to_string(index=False))


if __name__ == "__main__":
    main()

