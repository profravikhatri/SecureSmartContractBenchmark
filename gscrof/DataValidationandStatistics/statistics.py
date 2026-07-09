# --------------------------------------------------------------------------
# Outlier Detection (Interquartile Range Method)
# --------------------------------------------------------------------------

def detect_outliers(
    df: pd.DataFrame,
    output_directory: Path = RESULTS_DIR
) -> pd.DataFrame:
    """
    Detect potential outliers using the Interquartile Range (IQR) method.

    Outliers are identified but not removed automatically.
    """

    metrics = [

        "gasUsed",

        "latencyMs",

        "blockNumber"

    ]

    outlier_records = []

    summary_records = []

    for metric in metrics:

        q1 = df[metric].quantile(0.25)

        q3 = df[metric].quantile(0.75)

        iqr = q3 - q1

        lower_limit = q1 - (1.5 * iqr)

        upper_limit = q3 + (1.5 * iqr)

        outliers = df[
            (df[metric] < lower_limit) |
            (df[metric] > upper_limit)
        ]

        summary_records.append({

            "Metric": metric,

            "Q1": round(q1, 4),

            "Q3": round(q3, 4),

            "IQR": round(iqr, 4),

            "LowerLimit": round(lower_limit, 4),

            "UpperLimit": round(upper_limit, 4),

            "OutlierCount": len(outliers)

        })

        if not outliers.empty:

            temp = outliers.copy()

            temp["Metric"] = metric

            outlier_records.append(temp)

    summary_df = pd.DataFrame(summary_records)

    summary_file = output_directory / "outlier_summary.csv"

    summary_df.to_csv(

        summary_file,

        index=False

    )

    if outlier_records:

        outlier_df = pd.concat(

            outlier_records,

            ignore_index=True

        )

    else:

        outlier_df = pd.DataFrame()

    outlier_file = output_directory / "outlier_records.csv"

    outlier_df.to_csv(

        outlier_file,

        index=False

    )

    print("\n====================================")

    print("Outlier Detection")

    print("====================================")

    print(summary_df)

    print(

        f"\nSummary exported to: {summary_file}"

    )

    print(

        f"Outlier records exported to: {outlier_file}"

    )

    return outlier_df