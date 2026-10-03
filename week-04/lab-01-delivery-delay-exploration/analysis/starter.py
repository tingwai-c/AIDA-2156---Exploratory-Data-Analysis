from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ORIGINAL STARTER CODE

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "delivery_delays.csv"
OUTPUT = ROOT / "output"

# Define the required columns in the dataset.
REQUIRED_COLUMNS = {
    "delivery_id",
    "delivery_window",
    "route_type",
    "delay_minutes",
    "package_weight_kg",
}


# Load the dataset and check its basic structure.
def load_and_validate() -> pd.DataFrame:
    """Load the authorized fictional data and complete basic integrity checks."""

    deliveries = pd.read_csv(DATA_FILE)

    assert set(deliveries.columns) == REQUIRED_COLUMNS, "Unexpected CSV columns."
    assert deliveries["delivery_id"].notna().all(), "delivery_id cannot be blank."
    assert deliveries["delivery_id"].is_unique, "delivery_id values must be unique."

    return deliveries


# Create a basic profile of the dataset.
def write_starter_profile(deliveries: pd.DataFrame) -> None:
    """Create starter evidence only; this is not the completed lab analysis."""

    profile = pd.DataFrame({
        "column": deliveries.columns,
        "rows": len(deliveries),

        # Count missing values in each column.
        "missing_values": [
            int(deliveries[column].isna().sum())
            for column in deliveries.columns
        ],

        # Count distinct non-missing values in each column.
        "distinct_values": [
            int(deliveries[column].nunique(dropna=True))
            for column in deliveries.columns
        ],
    })

    profile.to_csv(
        OUTPUT / "starter_profile.csv",
        index=False
    )


def main() -> None:

    # Create the output folder and load the dataset.
    OUTPUT.mkdir(exist_ok=True)
    deliveries = load_and_validate()


# ============================================================================================================
# LAB PART 1 — Convert delay_minutes and identify missing values
  

    # Convert delay_minutes to numeric values.
    deliveries["delay_minutes"] = pd.to_numeric(
        deliveries["delay_minutes"],
        errors="coerce"
    )

    # Count missing values and keep usable delay values.
    missing_delay_count = deliveries["delay_minutes"].isna().sum()
    usable_delay = deliveries["delay_minutes"].dropna()


# =====================================================================================================
# LAB PART 2 — Create the required delay summary

    # Calculate the required summary statistics.
    usable_count = usable_delay.count()
    mean_delay = usable_delay.mean()
    median_delay = usable_delay.median()
    min_delay = usable_delay.min()
    max_delay = usable_delay.max()
    q1 = usable_delay.quantile(0.25)
    q3 = usable_delay.quantile(0.75)
    iqr = q3 - q1


# =====================================================================================================
# LAB PART 3 — Calculate the IQR upper fence

    # Calculate the upper fence for possible high-delay records.
    upper_fence = q3 + 1.5 * iqr


# =========================================================================================================
# LAB PART 2 — Build and save the delay summary

    # Build the summary table.
    delay_summary = pd.DataFrame({
        "statistic": [
            "usable_count",
            "mean",
            "median",
            "minimum",
            "maximum",
            "q1",
            "q3",
            "iqr",
            "upper_fence"
        ],
        "value": [
            usable_count,
            mean_delay,
            median_delay,
            min_delay,
            max_delay,
            q1,
            q3,
            iqr,
            upper_fence
        ],
    })

    # Save the summary table.
    delay_summary.to_csv(
        OUTPUT / "delay_summary.csv",
        index=False
    )


# =====================================================================================================
# LAB PART 3 — Flag possible high-delay records

    # Keep records above the IQR upper fence.
    possible_high_delays = deliveries[
        deliveries["delay_minutes"] > upper_fence
    ]

    # Save the possible high-delay records.
    possible_high_delays.to_csv(
        OUTPUT / "possible_high_delays.csv",
        index=False
    )

    # Print key results for checking.
    print(f"IQR upper fence: {upper_fence}")
    print(possible_high_delays)
    print(delay_summary)
    print(f"Missing delay_minutes values: {missing_delay_count}")


# ============================================================================================================
# ORIGINAL STARTER OUTPUT

    # Create the starter profile and print confirmation messages.
    write_starter_profile(deliveries)

    print(
        f"Starter checks passed for "
        f"{len(deliveries)} fictional delivery-stop records."
    )

    print("Created output/starter_profile.csv.")
    print(
        "Next: complete the guided delay analysis "
        "and one independent univariate analysis."
    )


# ============================================================================================================
# LAB PART 4 — Create the histogram and box plot
  
    # Create one figure with a histogram and box plot.
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(10, 4)
    )

    # Create the histogram.
    axes[0].hist(
        usable_delay,
        bins=8,
        edgecolor="black"
    )

    axes[0].set_title("Distribution of Delivery Delays")
    axes[0].set_xlabel("Delay (minutes)")
    axes[0].set_ylabel("Number of Deliveries")

    # Create the box plot.
    axes[1].boxplot(
        usable_delay,
        orientation="vertical"
    )

    axes[1].set_title("Delivery Delay Box Plot")
    axes[1].set_ylabel("Delay (minutes)")

    # Save the two charts in one image.
    plt.tight_layout()
    plt.savefig(
        OUTPUT / "delay_charts.png",
        dpi=150
    )
    plt.close()


# ===========================================================================================================
# LAB PART 5 — Independent analysis using delivery_window
   
    # Count the number of deliveries in each delivery window.
    delivery_window_counts = deliveries[
        "delivery_window"
    ].value_counts(
        dropna=False
    )

    # Calculate the percentage of deliveries in each delivery window.
    delivery_window_percentages = (
        deliveries["delivery_window"]
        .value_counts(
            dropna=False,
            normalize=True
        )
        .mul(100)
        .round(1)
    )

    # Convert the counts and percentages into a labelled summary table.
    delivery_window_summary = pd.DataFrame({
        "delivery_window": delivery_window_counts.index,
        "delivery_count": delivery_window_counts.values,
        "percentage": delivery_window_percentages.values,
    })

    # Save the independent-analysis summary.
    delivery_window_summary.to_csv(
        OUTPUT / "delivery_window_summary.csv",
        index=False
    )

    print(delivery_window_summary)

    # Create a bar chart for delivery_window.
    ax = delivery_window_counts.plot(
        kind="bar",
        figsize=(7, 4),
        edgecolor="black"
    )

    ax.set_title("Deliveries by Delivery Window")
    ax.set_xlabel("Delivery Window")
    ax.set_ylabel("Number of Deliveries")

    # Save the bar chart.
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(
        OUTPUT / "delivery_window_chart.png",
        dpi=150
    )
    plt.close()


if __name__ == "__main__":
    main()