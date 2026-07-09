# --------------------------------------------------------------------------
# Hypothesis Testing
# --------------------------------------------------------------------------

from scipy.stats import ttest_rel, wilcoxon


def hypothesis_testing(
    df: pd.DataFrame,
    normality_df: pd.DataFrame,
    output_directory: Path = RESULTS_DIR,
    alpha: float = 0.05
) -> pd.DataFrame:
    """
    Perform statistical hypothesis testing between the
    BaselineContract and ProposedFramework.

    The statistical test is selected automatically using the
    normality assessment.
    """

    metrics = [

        "gasUsed",

        "latencyMs"

    ]

    baseline = (

        df[df["contract"] == "BaselineContract"]

        .sort_values("iteration")

        .reset_index(drop=True)

    )

    proposed = (

        df[df["contract"] == "ProposedFramework"]

        .sort_values("iteration")

        .reset_index(drop=True)

    )

    if len(baseline) != len(proposed):

        raise ValueError(

            "Baseline and Proposed datasets must "

            "contain equal benchmark iterations."

        )

    results = []

    print("\n====================================")
    print("Hypothesis Testing")
    print("====================================")

    for metric in metrics:

        recommendation = normality_df.loc[

            normality_df["Metric"] == metric,

            "RecommendedTest"

        ].values[0]

        baseline_values = baseline[metric]

        proposed_values = proposed[metric]

        if recommendation == "Paired t-test":

            statistic, p_value = ttest_rel(

                baseline_values,

                proposed_values

            )

            test_used = "Paired t-test"

        else:

            statistic, p_value = wilcoxon(

                baseline_values,

                proposed_values

            )

            test_used = "Wilcoxon Signed-Rank"

        significant = (

            "Yes"

            if p_value < alpha

            else "No"

        )

        results.append({

            "Metric": metric,

            "Test": test_used,

            "Statistic": round(float(statistic), 6),

            "PValue": round(float(p_value), 6),

            "Alpha": alpha,

            "Significant": significant,

            "Decision":

                "Reject H0"

                if p_value < alpha

                else "Fail to Reject H0"

        })

    hypothesis_df = pd.DataFrame(results)

    output_file = (

        output_directory /

        "hypothesis_test.csv"

    )

    hypothesis_df.to_csv(

        output_file,

        index=False

    )

    print(hypothesis_df)

    print(

        f"\nHypothesis test exported to: {output_file}"

    )

    return hypothesis_df