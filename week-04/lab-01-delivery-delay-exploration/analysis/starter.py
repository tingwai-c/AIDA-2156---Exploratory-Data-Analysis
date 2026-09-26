from pathlib import Path  # Import Path for file and folder paths. / 导入 Path，用来处理文件和文件夹路径。
import pandas as pd  # Import pandas for data analysis. / 导入 pandas，用于数据分析。
import matplotlib.pyplot as plt  # Import matplotlib for charts. / 导入 matplotlib，用于绘图。

# ORIGINAL STARTER CODE / 老师原始 starter code

ROOT = Path(__file__).resolve().parents[1]  # Point to the main lab folder. / 指向整个 Lab 的主文件夹。
DATA_FILE = ROOT / "data" / "delivery_delays.csv"  # Point to the supplied CSV file. / 指向老师提供的 CSV 数据文件。
OUTPUT = ROOT / "output"  # Point to the output folder. / 指向保存结果的 output 文件夹。

# Define the exact columns expected in the CSV file. /  定义 CSV 文件中应该存在的所有列。
REQUIRED_COLUMNS = {
    "delivery_id",
    "delivery_window",
    "route_type",
    "delay_minutes",
    "package_weight_kg",
}

# Load data and check integrity. / 读取数据并检查完整性。
def load_and_validate() -> pd.DataFrame:
    """Load the authorized fictional data and complete basic integrity checks."""  

    deliveries = pd.read_csv(DATA_FILE)  # Read the CSV into a DataFrame. / 将 CSV 读取为 DataFrame。
    assert set(deliveries.columns) == REQUIRED_COLUMNS, "Unexpected CSV columns."  # Check expected columns. / 检查列名是否符合要求。
    assert deliveries["delivery_id"].notna().all(), "delivery_id cannot be blank."  # Check delivery_id has no blanks. / 检查 delivery_id 没有空值。
    assert deliveries["delivery_id"].is_unique, "delivery_id values must be unique."  # Check delivery_id is unique. / 检查 delivery_id 是否唯一。
    return deliveries  # Return the validated dataset. / 返回完成检查的数据。

# Create starter evidence only. / 只创建 starter 检查结果。
def write_starter_profile(deliveries: pd.DataFrame) -> None:
    """Create starter evidence only; this is not the completed lab analysis."""  

    # Build the starter profile table. /  创建 starter 数据概况表。
    profile = pd.DataFrame({
        "column": deliveries.columns,  # Store column names. / 保存列名。
        "rows": len(deliveries),  # Store total row count. / 保存总行数。

        # Count missing values in each column. / 计算每一列的缺失值数量。
        "missing_values": [
            int(deliveries[column].isna().sum())
            for column in deliveries.columns
        ],

        # Count distinct non-missing values in each column. / 计算每一列不同的非缺失值数量。
        "distinct_values": [
            int(deliveries[column].nunique(dropna=True))
            for column in deliveries.columns
        ],
    })

    profile.to_csv(OUTPUT / "starter_profile.csv", index=False)  # Save starter profile to CSV. / 将 starter profile 保存为 CSV。


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)  # Create output folder if needed. / 如果 output 文件夹不存在就创建。
    deliveries = load_and_validate()  # Load and validate the dataset. / 读取并验证数据。

# ==================================================================================================================================================
    # LAB PART 1 — Convert delay_minutes and identify missing values.
    # 作业第 1 部分 —— 转换 delay_minutes 并识别缺失值。

    # Convert delay_minutes to numeric; invalid values become NaN. /  将 delay_minutes 转换成数字；无法转换的值变成 NaN。
    deliveries["delay_minutes"] = pd.to_numeric(
        deliveries["delay_minutes"],
        errors="coerce"
    )

    missing_delay_count = deliveries["delay_minutes"].isna().sum()  # Count missing delay values. / 计算缺失的 delay 值数量。
    usable_delay = deliveries["delay_minutes"].dropna()  # Keep non-missing delays for analysis. / 保留非缺失的 delay 值用于分析。

# ==================================================================================================================================================
    # LAB PART 2 — Create the required delay summary.
    # 作业第 2 部分 —— 创建 delay 统计摘要。

    usable_count = usable_delay.count()  # Count usable delay values. / 计算可用 delay 值数量。
    mean_delay = usable_delay.mean()  # Calculate mean delay. / 计算平均延迟。
    median_delay = usable_delay.median()  # Calculate median delay. / 计算延迟中位数。
    min_delay = usable_delay.min()  # Calculate minimum delay. / 计算最小延迟。
    max_delay = usable_delay.max()  # Calculate maximum delay. / 计算最大延迟。
    q1 = usable_delay.quantile(0.25)  # Calculate Q1, the 25th percentile. / 计算 Q1，也就是第 25 百分位数。
    q3 = usable_delay.quantile(0.75)  # Calculate Q3, the 75th percentile. / 计算 Q3，也就是第 75 百分位数。
    iqr = q3 - q1  # Calculate IQR = Q3 - Q1. / 计算 IQR = Q3 - Q1。
    # LAB PART 3 — Calculate the IQR upper fence. /  作业第 3 部分 —— 计算 IQR 上界。
    upper_fence = q3 + 1.5 * iqr  # Calculate upper fence = Q3 + 1.5 × IQR. / 计算上界 = Q3 + 1.5 × IQR。

    # LAB PART 2 — Build and save delay summary.
    # 作业第 2 部分 —— 创建并保存 delay summary。

    # Build the required summary table. /  创建老师要求的统计摘要表。
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
            "upper_fence" # LAB PART 3 
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
            upper_fence # LAB PART 3 
        ],
    })

# ==================================================================================================================================================
    # LAB PART 3 — Flag possible high-delay records.
    # 作业第 3 部分 —— 标记可能的高延迟记录。

    # Keep rows where delay_minutes is above the upper fence. /  保留 delay_minutes 高于 upper fence 的记录。
    possible_high_delays = deliveries[
        deliveries["delay_minutes"] > upper_fence
    ]

    # Save flagged records for review. /  将被标记的记录保存下来供检查。
    possible_high_delays.to_csv(
        OUTPUT / "possible_high_delays.csv",
        index=False
    )

    print(f"IQR upper fence: {upper_fence}")  # Print the upper fence. / 打印 IQR upper fence。
    print(possible_high_delays)  # Print flagged high-delay records. / 打印被标记的高延迟记录。

# ================================================================================================================================================== 
    # LAB PART 2 — Save delay_summary.csv. /  作业第 2 部分 —— 保存 delay_summary.csv。

    # Save summary statistics to CSV. /  将统计摘要保存为 CSV。
    delay_summary.to_csv(
        OUTPUT / "delay_summary.csv",
        index=False
    )

    print(delay_summary)  # Print the summary table. / 打印统计摘要表。
    print(f"Missing delay_minutes values: {missing_delay_count}")  # Print missing delay count. / 打印缺失 delay 的数量。


    # ORIGINAL STARTER CODE / 老师原始 starter code
    write_starter_profile(deliveries)  # Create starter_profile.csv. / 创建 starter_profile.csv。
    print(f"Starter checks passed for {len(deliveries)} fictional delivery-stop records.")  # Print validated row count. / 打印通过检查的记录数量。
    print("Created output/starter_profile.csv.")  # Confirm starter profile output. / 确认 starter profile 已生成。
    print("Next: complete the guided delay analysis and one independent univariate analysis.")  # Show the next task reminder. / 显示下一步任务提醒。

# ==================================================================================================================================================
    # LAB PART 4 — Create the required histogram and box plot.
    # 作业第 4 部分 —— 创建老师要求的直方图和箱线图。

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))  # Create one figure with two side-by-side charts. / 创建一张包含两个并排图表的画布。

    axes[0].hist(usable_delay, bins=8, edgecolor="black")  # Create a histogram of usable delay values. / 创建可用 delay 数据的直方图。
    axes[0].set_title("Distribution of Delivery Delays")  # Add histogram title. / 添加直方图标题。
    axes[0].set_xlabel("Delay (minutes)")  # Label the x-axis. / 设置 x 轴标签。
    axes[0].set_ylabel("Number of Deliveries")  # Label the y-axis. / 设置 y 轴标签。

    axes[1].boxplot(usable_delay, orientation="vertical")  # Create a vertical box plot. / 创建纵向箱线图。
    axes[1].set_title("Delivery Delay Box Plot")  # Add box plot title. / 添加箱线图标题。
    axes[1].set_ylabel("Delay (minutes)")  # Label the y-axis. / 设置 y 轴标签。

    plt.tight_layout()  # Adjust spacing so labels do not overlap. / 自动调整间距，避免标题和标签重叠。

    plt.savefig(OUTPUT / "delay_charts.png", dpi=150)  # Save both charts as the required PNG file. / 将两个图保存为老师要求的 PNG 文件。

    plt.close()  # Close the figure after saving it. / 保存后关闭图表，避免重复占用内存。

#=================================================================================================================================================================
    # LAB PART 5 — Independent analysis using delivery_window.
    # 作业第 5 部分 —— 使用 delivery_window 做独立单变量分析。

    delivery_window_counts = deliveries["delivery_window"].value_counts(dropna=False)  # Count deliveries in each delivery window. / 计算每个 delivery window 有多少条记录。

    # Convert the counts into a DataFrame for a clear labelled output.
    # 将计数结果转换成 DataFrame，方便保存成清楚的表格。
    delivery_window_summary = delivery_window_counts.rename_axis(
        "delivery_window"
    ).reset_index(
        name="delivery_count"
    )

    # Save the independent-analysis summary table.
    # 保存独立分析的统计表。
    delivery_window_summary.to_csv(
        OUTPUT / "delivery_window_summary.csv",
        index=False
    )

    print(delivery_window_summary)  # Print the independent-analysis summary. / 打印独立分析结果。


    # Create a bar chart for the categorical delivery_window variable.
    # 为分类变量 delivery_window 创建柱状图。
    ax = delivery_window_counts.plot(
        kind="bar",
        figsize=(7, 4),
        edgecolor="black"
    )

    ax.set_title("Deliveries by Delivery Window")  # Add chart title. / 添加图表标题。
    ax.set_xlabel("Delivery Window")  # Label the x-axis. / 设置 x 轴标签。
    ax.set_ylabel("Number of Deliveries")  # Label the y-axis. / 设置 y 轴标签。

    plt.xticks(rotation=0)  # Keep category labels horizontal. / 让分类名称保持水平显示。
    plt.tight_layout()  # Adjust spacing to avoid overlap. / 自动调整间距避免重叠。
    plt.savefig(OUTPUT / "delivery_window_chart.png", dpi=150)  # Save the bar chart. / 保存柱状图。
    plt.close()  # Close the chart after saving. / 保存后关闭图表。


if __name__ == "__main__":
    main()  # Run main() when this file is executed directly. / 直接运行这个文件时执行 main()。