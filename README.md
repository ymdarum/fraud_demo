# Corporate Payment Liquidity Fraud Demo (Local)

This is a **small end-to-end demo** you can run on your laptop to show:

- A synthetic **corporate treasury payment stream**
- An **AI anomaly detection model** (Isolation Forest)
- A **risk score (0 → 1)** per transaction
- A **fraud monitoring dashboard** (Streamlit)

The goal is to be **simple, explainable, and visually impressive** for stakeholders.

---

## Project layout

This repo follows a simple "frontend / backend" split.

- `backend/`
  - `payment_simulator.py`: generates `dataset.csv` (normal + injected fraud-like cases)
  - `fraud_model.py`: reads `dataset.csv`, scores anomalies, writes `dataset_scored.csv`
  - `dashboard.py`: Streamlit dashboard to explore alerts
  - `requirements.txt`: Python dependencies
- `frontend/`
  - (not used in this demo yet)

---

## Prerequisites

- Windows (works on macOS/Linux too)
- Python installed (3.10+ recommended)

---

## Setup

Do this once from the **project root** (the folder that contains `backend/`).

1. **Create a virtual environment**

   ```bash
   python -m venv .venv
   ```

2. **Activate it** (pick one for your OS/shell)
   - **Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
   - **Windows (CMD):** `.\.venv\Scripts\activate.bat`
   - **macOS / Linux:** `source .venv/bin/activate`

3. **Install dependencies**

   ```bash
   pip install -r backend/requirements.txt
   ```

---

## Run the demo

Run these **in order** from the project root, with the virtual environment **activated**.

| Step | Command | What it does |
|------|---------|--------------|
| 1 | `python backend/payment_simulator.py` | Creates `dataset.csv` (synthetic payments). |
| 2 | `python backend/fraud_model.py` | Creates `dataset_scored.csv` (risk scores). Prints top risky transactions. |
| 3 | `streamlit run backend/dashboard.py` | Starts the dashboard. Open the URL shown in the terminal (e.g. http://localhost:8501). |

**Summary:** Generate data → Score with the model → View results in the dashboard.

---

## What stakeholders will see

### Storyline

1. Corporate payments are processed (simulated dataset).
2. AI analyzes transaction behavior (simple engineered features).
3. AI calculates a fraud risk score (0 to 1).
4. Suspicious liquidity movement is flagged in a dashboard.

### Example (typical injected fraud-like pattern)

- Very large payment amount (RM 15M – 40M)
- Unusual payment hour (1 AM – 4 AM)
- Suspicious new beneficiary (“Unknown Offshore Ltd”)
- Higher-risk country corridor (HK)

---

## Notes (important for learning)

- This is a **demo**. Real fraud systems need:
  - Better data (beneficiary history, approval chains, device signals, user behavior)
  - Strong governance + explainability + audit trails
  - Continuous monitoring and retraining
- We keep the features and model intentionally simple so you can explain it clearly.

