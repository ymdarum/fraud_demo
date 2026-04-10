# Corporate Payment Liquidity Fraud Demo (Local)

This is a **small end-to-end demo** you can run on your laptop to show:

- A synthetic **corporate treasury payment stream**
- An **AI anomaly detection model** (Isolation Forest)
- A **risk score (0 → 1)** per transaction
- A **fraud monitoring dashboard** (Streamlit)

The goal is to be **simple, explainable, and visually impressive** for stakeholders.

---

## Project layout

Current runnable app is in `backend/`:

- `backend/payment_simulator.py`: generates `dataset.csv` (normal + injected fraud-like cases)
- `backend/fraud_model.py`: reads `dataset.csv`, scores anomalies, writes `dataset_scored.csv`
- `backend/dashboard.py`: Streamlit dashboard to explore alerts
- `backend/requirements.txt`: Python dependencies

Note: there is no runnable frontend app in this repository yet.

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

## Quickstart (PowerShell)

From the project root (`gib/`), run:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
python backend/payment_simulator.py
python backend/fraud_model.py
streamlit run backend/dashboard.py
```

Open the URL shown by Streamlit (usually <http://localhost:8501>).

---

## Run the demo (step-by-step)

Run these commands **in order** from the project root, with the virtual environment **activated**.

| Step | Command | What it does |
|------|---------|--------------|
| 1 | `python backend/payment_simulator.py` | Creates `dataset.csv` in the project root (synthetic payments). |
| 2 | `python backend/fraud_model.py` | Reads `dataset.csv` and creates `dataset_scored.csv` in the project root. |
| 3 | `streamlit run backend/dashboard.py` | Starts the dashboard. |

Why run from project root: scripts use relative paths like `dataset.csv`, so running from root keeps paths consistent.

---

## How to verify it is working

1. After step 1, confirm `dataset.csv` exists in the project root.
2. After step 2, confirm `dataset_scored.csv` exists in the project root.
3. In the dashboard:
   - Move the **Risk Threshold** slider.
   - Confirm the suspicious transaction table updates.
   - Confirm at least one high-risk alert appears at a lower threshold (for example `0.60`).

---

## Troubleshooting

- **`ModuleNotFoundError`**: virtual environment may not be activated. Activate `.venv` and reinstall requirements.
- **`streamlit` command not found**: run `pip install -r backend/requirements.txt` again inside the activated `.venv`.
- **Dashboard says file not found**: generate data first by running steps 1 and 2.
- **PowerShell script execution blocked**: run PowerShell as admin once and allow local scripts:
  - `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
  - Then activate: `.\.venv\Scripts\Activate.ps1`

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

