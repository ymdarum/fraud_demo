"""
payment_simulator.py

This script generates a synthetic "corporate treasury payments" dataset.
It is meant for demos, not for real production fraud detection.

What it does (high level):
- Creates many "normal" corporate payments (typical amounts + typical office hours).
- Injects a small number of "fraud-like" payments (very large amount, odd hour, risky country,
  suspicious new beneficiary).

Output:
- Writes a CSV file: dataset.csv

How to run:
  python backend/payment_simulator.py
"""

from __future__ import annotations

import random
from dataclasses import dataclass

import pandas as pd
from faker import Faker


@dataclass(frozen=True)
class SimulatorConfig:
    """
    Small config object to keep the generator easy to tweak.
    """

    normal_txn_count: int = 500
    fraud_txn_count: int = 10
    seed: int = 42
    output_csv: str = "dataset.csv"


def generate_payments(config: SimulatorConfig) -> pd.DataFrame:
    """
    Generate a DataFrame of synthetic corporate payments.

    We keep the schema simple on purpose so stakeholders can understand it quickly.
    """

    # Deterministic randomness makes the demo repeatable (same output each run).
    random.seed(config.seed)
    faker = Faker()
    Faker.seed(config.seed)

    companies = ["ABC Corp", "Mega Manufacturing", "Global Trading"]
    countries = ["MY", "SG", "US", "HK", "CN"]

    rows: list[dict] = []

    # 1) Normal corporate payments.
    for i in range(config.normal_txn_count):
        company = random.choice(companies)

        # Normal amounts: RM100k to RM3m (range from the prompt).
        amount = random.randint(100_000, 3_000_000)

        # Beneficiary is typically "some known company". Faker provides realistic names.
        beneficiary = faker.company()

        # Countries: mix of normal and occasionally risky.
        country = random.choice(countries)

        # Most corporate payments happen during office hours.
        hour = random.randint(9, 18)

        # Corporate liquidity / balance (bigger than payment, typically).
        balance = random.randint(20_000_000, 100_000_000)

        rows.append(
            {
                "txn_id": i,
                "company": company,
                "amount": amount,
                "beneficiary": beneficiary,
                "country": country,
                "hour": hour,
                "balance": balance,
                # Helpful for demos: we keep a "ground truth" label so you can explain
                # that the model should (hopefully) rank these higher risk.
                "is_injected_fraud": 0,
            }
        )

    # 2) Inject fraud-like scenarios.
    #
    # These are NOT "proof of fraud" in real life. They are suspicious patterns that
    # often correlate with liquidity fraud:
    # - very large payment compared to typical size
    # - new / unknown beneficiary
    # - unusual hour (e.g., 1 AM - 4 AM)
    # - higher-risk country corridor
    start_id = config.normal_txn_count
    for j in range(config.fraud_txn_count):
        rows.append(
            {
                "txn_id": start_id + j,
                "company": "ABC Corp",
                "amount": random.randint(15_000_000, 40_000_000),
                "beneficiary": "Unknown Offshore Ltd",
                "country": "HK",
                "hour": random.randint(1, 4),
                "balance": 50_000_000,
                "is_injected_fraud": 1,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    config = SimulatorConfig()
    df = generate_payments(config)

    # We save into the project root by default (easy for Streamlit + scripts to find).
    df.to_csv(config.output_csv, index=False)
    print(f"Dataset created: {config.output_csv} (rows={len(df)})")


if __name__ == "__main__":
    main()

