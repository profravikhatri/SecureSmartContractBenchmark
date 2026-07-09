"""
-----------------------------------------------------------------------------
SecureSmartContractBenchmark

Module:
    Gas Consumption Analysis

Description:
    Performs comprehensive gas consumption analysis for the
    baseline and proposed blockchain frameworks.

Outputs:

results/

    gas_summary.csv

    gas_distribution.csv

    gas_statistics.csv

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

        "gasUsed"

    ]

    missing = [

        c for c in required

        if c not in df.columns

    ]

    if missing:

        raise ValueError(

            "Missing Columns:\n"

            + "\n".join(missing)

        )


# --------------------------------------------------------------------------
# Gas Summary
# --------------------------------------------------------------------------

def gas_summary(df):

    summary = (

        df.groupby("contract")["gasUsed"]

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

        "MeanGas",

        "MedianGas",

        "MinimumGas",

        "MaximumGas",

        "StandardDeviation"

    ]

    summary.to_csv(

        RESULTS_DIR /

        "gas_summary.csv",

        index=False

    )

    return summary


# --------------------------------------------------------------------------
# Gas Reduction
# --------------------------------------------------------------------------

def gas_reduction(df):

    baseline = (

        df[

            df["contract"]

            == "BaselineContract"

        ]["gasUsed"]

        .mean()

    )

    proposed = (

        df[

            df["contract"]

            == "ProposedFramework"

        ]["gasUsed"]

        .mean()

    )

    reduction = (

        (baseline - proposed)

        /

        baseline

    ) * 100

    statistics = pd.DataFrame([{

        "BaselineAverageGas":

            round(baseline,2),

        "ProposedAverageGas":

            round(proposed,2),

        "GasReductionPercent":

            round(reduction,2)

    }])

    statistics.to_csv(

        RESULTS_DIR /

        "gas_statistics.csv",

        index=False

    )

    return statistics


# --------------------------------------------------------------------------
# Gas Distribution
# --------------------------------------------------------------------------

def gas_distribution(df):

    distribution = (

        df.groupby([

            "contract",

            "gasUsed"

        ])

        .size()

        .reset_index(name="Frequency")

    )

    distribution.to_csv(

        RESULTS_DIR /

        "gas_distribution.csv",

        index=False

    )

    return distribution


# --------------------------------------------------------------------------
# Percentiles
# --------------------------------------------------------------------------

def gas_percentiles(df):

    records = []

    for contract in df["contract"].unique():

        values = df[

            df["contract"] == contract

        ]["gasUsed"]

        records.append({

            "Contract": contract,

            "25Percentile":

                round(values.quantile(0.25),2),

            "50Percentile":

                round(values.quantile(0.50),2),

            "75Percentile":

                round(values.quantile(0.75),2),

            "95Percentile":

                round(values.quantile(0.95),2)

        })

    percentile_df = pd.DataFrame(records)

    percentile_df.to_csv(

        RESULTS_DIR /

        "gas_percentiles.csv",

        index=False

    )

    return percentile_df


# --------------------------------------------------------------------------
# Main Analysis
# --------------------------------------------------------------------------

def run_gas_analysis():

    print("\n====================================")

    print("Gas Consumption Analysis")

    print("====================================")

    df = load_dataset()

    validate_dataset(df)

    summary = gas_summary(df)

    reduction = gas_reduction(df)

    distribution = gas_distribution(df)

    percentiles = gas_percentiles(df)

    print("\nGas Summary")

    print(summary)

    print("\nGas Reduction")

    print(reduction)

    print("\nPercentiles")

    print(percentiles)

    print("\nAnalysis completed.\n")


if __name__ == "__main__":

    run_gas_analysis()
