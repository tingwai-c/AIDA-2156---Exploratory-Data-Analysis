from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "service_dispatches.csv"
OUTPUT_DIR = ROOT / "output"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    # TODO 1: State the row grain in your decision note.
    # TODO 2: Check missingness in job_difficulty_score, technician_hours, and service_region.
    # TODO 3: Create a scatter plot and save it in output/.
    # TODO 4: Create a grouped region summary and save it in output/.
    # TODO 5: Write output/decision_note.md using only evidence from your analysis.

    print(df.head())
    print(df[["job_difficulty_score", "technician_hours", "service_region"]].isna().sum())


if __name__ == "__main__":
    main()
