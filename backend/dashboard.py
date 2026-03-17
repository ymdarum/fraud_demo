"""
dashboard.py (Streamlit)

This is a simple fraud monitoring dashboard for the demo.

What stakeholders can do:
- Move a risk threshold slider (0→1)
- Immediately see which transactions are above that threshold
- See a simple "risk score distribution" chart

How to run:
  streamlit run backend/dashboard.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


def load_data(path: str) -> pd.DataFrame:
    """
    Load the scored dataset.

    We keep this in a function so beginners can see a clean separation:
    data loading vs UI rendering.
    """

    df = pd.read_csv(path)
    return df


def main() -> None:
    st.set_page_config(page_title="Corporate Payment Fraud Monitor", layout="wide")

    st.title("Corporate Payment Fraud Monitor")
    st.write(
        """
This dashboard shows a synthetic corporate payment stream scored by an AI anomaly model.

- **Risk score** is a number from **0 to 1**.
- Higher means **more suspicious** (more anomalous liquidity movement).
        """
    )

    data_path = st.sidebar.text_input("Scored dataset path", value="dataset_scored.csv")
    df = load_data(data_path)

    st.sidebar.header("Controls")
    threshold = st.sidebar.slider("Risk Threshold", 0.0, 1.0, 0.7, 0.01)

    st.subheader("Risk score distribution (quick heatmap-style view)")
    st.bar_chart(df["risk_score"])

    alerts = df[df["risk_score"] > threshold].copy()

    st.subheader("Suspicious Transactions")
    st.write(f"Showing **{len(alerts)}** transactions with **risk_score > {threshold:.2f}**.")

    # Make the table easy to scan: show the key fields first.
    show_cols = [
        "txn_id",
        "company",
        "amount",
        "beneficiary",
        "country",
        "hour",
        "balance",
        "payment_ratio",
        "unusual_hour",
        "high_risk_country",
        "risk_score",
        "fraud_flag",
        "is_injected_fraud",
    ]

    # If the CSV is missing columns (e.g., user loaded a wrong file),
    # we fall back to whatever exists to avoid a confusing crash.
    show_cols_existing = [c for c in show_cols if c in df.columns]
    st.dataframe(alerts[show_cols_existing], use_container_width=True)

    st.subheader("Example alert card (for storytelling)")
    if len(alerts) == 0:
        st.info("No alerts above the threshold. Try lowering the threshold.")
    else:
        top = alerts.sort_values("risk_score", ascending=False).iloc[0]
        st.warning(
            "\n".join(
                [
                    "⚠ Fraud Alert",
                    f"Transaction: RM{int(top['amount']):,}",
                    f"Beneficiary: {top.get('beneficiary', 'N/A')}",
                    f"Country: {top.get('country', 'N/A')}",
                    f"Time (hour): {top.get('hour', 'N/A')}",
                    f"Risk Score: {float(top['risk_score']):.2f}",
                ]
            )
        )


if __name__ == "__main__":
    main()

