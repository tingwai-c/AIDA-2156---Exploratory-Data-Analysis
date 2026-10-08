from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "service_dispatches.csv"
OUTPUT_DIR = ROOT / "output"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    # State the row grain
    print("One row represents one completed field-service dispatch.")

    # Check missing values in the analysis fields
    missing_values = df[
        ["job_difficulty_score", "technician_hours", "service_region"]
    ].isna().sum()

    print("\nFirst five rows:")
    print(df.head())

    print("\nMissing values:")
    print(missing_values)

    # Create a scatter plot by service region
    plt.figure(figsize=(8, 6))

    for region in df["service_region"].unique():
        region_data = df[df["service_region"] == region]

        plt.scatter(
            region_data["job_difficulty_score"],
            region_data["technician_hours"],
            label=region
        )

    plt.xlabel("Job Difficulty Score")
    plt.ylabel("Technician Hours")
    plt.title("Job Difficulty Score vs Technician Hours")
    plt.legend(title="Service Region")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "dispatch_relationships.png")
    plt.close()

    # Create a grouped summary by service region
    region_summary = (
        df.groupby("service_region")["technician_hours"]
        .agg(["count", "mean", "median"])
        .reset_index()
    )

    region_summary.to_csv(
        OUTPUT_DIR / "region_summary.csv",
        index=False
    )

    print("\nRegion summary:")
    print(region_summary)


if __name__ == "__main__":
    main()