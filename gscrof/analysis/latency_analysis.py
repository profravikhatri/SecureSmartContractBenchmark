"""
-----------------------------------------------------------------------------
SecureSmartContractBenchmark

Module:
    Latency Analysis

Description:
    Performs latency analysis for blockchain benchmark experiments.

Outputs:

results/

    latency_summary.csv
    latency_statistics.csv
    latency_distribution.csv
    latency_percentiles.csv

-----------------------------------------------------------------------------
"""

from pathlib import Path
import pandas as pd
import numpy as np

RESULTS_DIR = Path("../results")

INPUT_FILE = RESULTS_DIR / "benchmark_results.csv"


# --------------------------------------------------------------------------
# Dataset Loader
# --------------------------------------------------------------------------

def load_dataset():

    if not INPUT_FILE.exists():

        raise FileNotFoundError(

            f"Benchmark file not found: {INPUT_FILE}"

        )

    return pd.read_csv(INPUT_FILE)


# --------------------------------------------------------------------------
# Dataset Validation
# --------------------------------------------------------------------------

def validate_dataset(df):

    required = [

        "contract",

        "iteration",

        "latencyMs"

    ]

    missing = [

        column

        for column in required

        if column not in df.columns

    ]

    if missing:

        raise ValueError(

            "Missing Columns:\n"

            + "\n".join(missing)

        )


# --------------------------------------------------------------------------
# Latency Summary
# --------------------------------------------------------------------------

def latency_summary(df):

    summary = (

        df.groupby("contract")["latencyMs"]

        .agg([

            "count",

            "mean",

            "median",

            "min",

            "max",

            "std"

        ])

        .reset_index()

    )

    summary.columns = [

        "Contract",

        "Observations",

        "AverageLatency(ms)",

        "MedianLatency(ms)",

        "MinimumLatency(ms)",

        "MaximumLatency(ms)",

        "StandardDeviation(ms)"

    ]

    summary.to_csv(

        RESULTS_DIR /

        "latency_summary.csv",

        index=False

    )

    return summary


# --------------------------------------------------------------------------
# Latency Improvement
# --------------------------------------------------------------------------

def latency_improvement(df):

    baseline = (

        df[

            df["contract"]

            == "BaselineContract"

        ]["latencyMs"]

        .mean()

    )

    proposed = (

        df[

            df["contract"]

            == "ProposedFramework"

        ]["latencyMs"]

        .mean()

    )

    improvement = (

        (baseline - proposed)

        /

        baseline

    ) * 100

    statistics = pd.DataFrame([{

        "BaselineAverageLatency(ms)":

            round(baseline,4),

        "ProposedAverageLatency(ms)":

            round(proposed,4),

        "LatencyImprovementPercent":

            round(improvement,2)

    }])

    statistics.to_csv(

        RESULTS_DIR /

        "latency_statistics.csv",

        index=False

    )

    return statistics


# --------------------------------------------------------------------------
# Latency Distribution
# --------------------------------------------------------------------------

def latency_distribution(df):

    distribution = (

        df.groupby([

            "contract",

            "latencyMs"

        ])

        .size()

        .reset_index(name="Frequency")

    )

    distribution.to_csv(

        RESULTS_DIR /

        "latency_distribution.csv",

        index=False

    )

    return distribution


# --------------------------------------------------------------------------
# Latency Percentiles
# --------------------------------------------------------------------------

def latency_percentiles(df):

    records = []

    for contract in sorted(df["contract"].unique()):

        values = df[

            df["contract"] == contract

        ]["latencyMs"]

        records.append({

            "Contract": contract,

            "25Percentile":

                round(values.quantile(0.25),4),

            "50Percentile":

                round(values.quantile(0.50),4),

            "75Percentile":

                round(values.quantile(0.75),4),

            "95Percentile":

                round(values.quantile(0.95),4)

        })

    percentile_df = pd.DataFrame(records)

    percentile_df.to_csv(

        RESULTS_DIR /

        "latency_percentiles.csv",

        index=False

    )

    return percentile_df


# --------------------------------------------------------------------------
# Latency Stability
# --------------------------------------------------------------------------

def latency_stability(df):

    records = []

    for contract in sorted(df["contract"].unique()):

        values = df[

            df["contract"] == contract

        ]["latencyMs"]

        mean = values.mean()

        std = values.std(ddof=1)

        cv = (

            (std / mean) * 100

            if mean > 0

            else 0

        )

        records.append({

            "Contract": contract,

            "CoefficientOfVariation(%)":

                round(cv,2)

        })

    stability_df = pd.DataFrame(records)

    stability_df.to_csv(

        RESULTS_DIR /

        "latency_stability.csv",

        index=False

    )

    return stability_df


# --------------------------------------------------------------------------
# Main Analysis
# --------------------------------------------------------------------------

def run_latency_analysis():

    print("\n====================================")

    print("Latency Analysis")

    print("====================================")

    df = load_dataset()

    validate_dataset(df)

    summary = latency_summary(df)

    improvement = latency_improvement(df)

    distribution = latency_distribution(df)

    percentiles = latency_percentiles(df)

    stability = latency_stability(df)

    print("\nLatency Summary")

    print(summary)

    print("\nLatency Improvement")

    print(improvement)

    print("\nLatency Stability")

    print(stability)

    print("\nLatency analysis completed.\n")


if __name__ == "__main__":

    run_latency_analysis()
