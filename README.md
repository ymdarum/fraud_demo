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

From the repo root:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
```

---

## Run the demo (end-to-end)

### 1) Generate synthetic payments

```bash
python backend/payment_simulator.py
```

This creates:

- `dataset.csv`

### 2) Train + score fraud risk

```bash
python backend/fraud_model.py
```

This creates:

- `dataset_scored.csv`

The script also prints the **top risky transactions** so you can immediately see the result.

### 3) Start the dashboard

```bash
streamlit run backend/dashboard.py
```

Open the local URL shown in the terminal (Streamlit prints it).

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

## Pushing to GitHub

The repo is ready to push. From the project root:

```bash
git add .
git commit -m "Initial commit: corporate payment fraud demo"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub username and repository name.  
Generated files (`dataset.csv`, `dataset_scored.csv`) and the virtual environment (`.venv/`) are in `.gitignore` and will not be committed.

---

## Notes (important for learning)

- This is a **demo**. Real fraud systems need:
  - Better data (beneficiary history, approval chains, device signals, user behavior)
  - Strong governance + explainability + audit trails
  - Continuous monitoring and retraining
- We keep the features and model intentionally simple so you can explain it clearly.

