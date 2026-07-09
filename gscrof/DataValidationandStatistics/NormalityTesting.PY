# --------------------------------------------------------------------------
# Normality Testing (Shapiro-Wilk Test)
# --------------------------------------------------------------------------

from scipy.stats import shapiro


def normality_test(
    df: pd.DataFrame,
    output_directory: Path = RESULTS_DIR,
    alpha: float = 0.05
) -> pd.DataFrame:
    """
    Perform Shapiro-Wilk normality testing for benchmark metrics.

    Parameters
    ----------
    df : pandas.DataFrame
        Validated benchmark dataset.

    output_directory : Path
        Directory where results are stored.

    alpha : float
        Significance level (default = 0.05).

    Returns
    -------
    pandas.DataFrame
        Normality test results.
    """

    metrics = [

        "gasUsed",

        "latencyMs",

        "blockNumber"

    ]

    results = []

    print("\n====================================")
    print("Normality Testing (Shapiro-Wilk)")
    print("====================================")

    for metric in metrics:

        statistic, p_value = shapiro(df[metric])

        if p_value >= alpha:

            distribution = "Normal"

            recommended_test = "Paired t-test"

        else:

            distribution = "Non-Normal"

            recommended_test = "Wilcoxon Signed-Rank"

        results.append({

            "Metric": metric,

            "Statistic": round(statistic, 6),

            "PValue": round(p_value, 6),

            "Alpha": alpha,

            "Distribution": distribution,

            "RecommendedTest": recommended_test

        })

    normality_df = pd.DataFrame(results)

    output_file = output_directory / "normality_test.csv"

    normality_df.to_csv(

        output_file,

        index=False

    )

    print(normality_df)

    print(f"\nResults exported to: {output_file}")

    return normality_df