# --------------------------------------------------------------------------
# Descriptive Statistics
# --------------------------------------------------------------------------

from typing import Dict


def descriptive_statistics(
    df: pd.DataFrame,
    output_directory: Path = RESULTS_DIR
) -> Dict:
    """
    Compute descriptive statistics for benchmark metrics.

    Parameters
    ----------
    df : pandas.DataFrame
        Validated benchmark dataset.

    output_directory : Path
        Directory where statistics are exported.

    Returns
    -------
    dict
        Dictionary containing descriptive statistics.
    """

    metrics = [

        "gasUsed",

        "latencyMs",

        "blockNumber"

    ]

    descriptive_summary = {}

    statistics_table = []

    for metric in metrics:

        values = df[metric]

        metric_statistics = {

            "Metric": metric,

            "Count": int(values.count()),

            "Mean": round(values.mean(), 4),

            "Median": round(values.median(), 4),

            "Mode": round(values.mode().iloc[0], 4)
            if not values.mode().empty
            else None,

            "Minimum": round(values.min(), 4),

            "Maximum": round(values.max(), 4),

            "Range": round(
                values.max() - values.min(),
                4
            ),

            "Variance": round(
                values.var(ddof=1),
                4
            ),

            "StandardDeviation": round(
                values.std(ddof=1),
                4
            ),

            "FirstQuartile": round(
                values.quantile(0.25),
                4
            ),

            "ThirdQuartile": round(
                values.quantile(0.75),
                4
            ),

            "InterQuartileRange": round(

                values.quantile(0.75)

                -

                values.quantile(0.25),

                4

            )

        }

        descriptive_summary[metric] = metric_statistics

        statistics_table.append(metric_statistics)

    descriptive_dataframe = pd.DataFrame(

        statistics_table

    )

    output_file = (

        output_directory /

        "descriptive_statistics.csv"

    )

    descriptive_dataframe.to_csv(

        output_file,

        index=False

    )

    print("\n====================================")

    print("Descriptive Statistics")

    print("====================================\n")

    print(descriptive_dataframe)

    print(

        f"\nStatistics exported to: {output_file}"

    )

    return descriptive_summary