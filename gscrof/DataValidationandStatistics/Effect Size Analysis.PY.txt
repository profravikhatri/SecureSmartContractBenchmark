# --------------------------------------------------------------------------
# Effect Size Analysis
# --------------------------------------------------------------------------

import numpy as np


def effect_size_analysis(
    df: pd.DataFrame,
    normality_df: pd.DataFrame,
    output_directory: Path = RESULTS_DIR
) -> pd.DataFrame:
    """
    Compute effect size between BaselineContract and
    ProposedFramework.

    Cohen's d is calculated for paired t-tests.

    Rank-Biserial Correlation is calculated for
    Wilcoxon Signed-Rank tests.
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

    results = []

    print("\n====================================")
    print("Effect Size Analysis")
    print("====================================")

    for metric in metrics:

        recommendation = normality_df.loc[

            normality_df["Metric"] == metric,

            "RecommendedTest"

        ].values[0]

        baseline_values = baseline[metric].to_numpy()

        proposed_values = proposed[metric].to_numpy()

        differences = baseline_values - proposed_values

        if recommendation == "Paired t-test":

            mean_difference = np.mean(differences)

            std_difference = np.std(

                differences,

                ddof=1

            )

            effect = (

                mean_difference /

                std_difference

            )

            method = "Cohen's d"

            magnitude = interpret_cohens_d(

                abs(effect)

            )

        else:

            statistic, _ = wilcoxon(

                baseline_values,

                proposed_values

            )

            n = len(differences)

            effect = (

                1 -

                (2 * statistic) /

                (n * (n + 1) / 2)

            )

            method = "Rank-Biserial Correlation"

            magnitude = interpret_rank_biserial(

                abs(effect)

            )

        results.append({

            "Metric": metric,

            "Method": method,

            "EffectSize": round(

                float(effect),

                4

            ),

            "Magnitude": magnitude

        })

    effect_df = pd.DataFrame(results)

    output_file = (

        output_directory /

        "effect_size.csv"

    )

    effect_df.to_csv(

        output_file,

        index=False

    )

    print(effect_df)

    print(

        f"\nEffect sizes exported to: {output_file}"

    )

    return effect_df


# --------------------------------------------------------------------------
# Cohen's d Interpretation
# --------------------------------------------------------------------------

def interpret_cohens_d(value: float) -> str:

    if value < 0.20:
        return "Negligible"

    elif value < 0.50:
        return "Small"

    elif value < 0.80:
        return "Medium"

    else:
        return "Large"


# --------------------------------------------------------------------------
# Rank-Biserial Interpretation
# --------------------------------------------------------------------------

def interpret_rank_biserial(value: float) -> str:

    if value < 0.10:
        return "Negligible"

    elif value < 0.30:
        return "Small"

    elif value < 0.50:
        return "Medium"

    else:
        return "Large"