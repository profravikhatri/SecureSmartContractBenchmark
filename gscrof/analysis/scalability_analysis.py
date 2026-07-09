"""
-----------------------------------------------------------------------------
SecureSmartContractBenchmark

Module:
    Scalability Analysis

Description:
    Evaluates scalability characteristics of the blockchain
    framework under increasing transaction workloads.

Outputs:

results/

    scalability_summary.csv
    throughput_results.csv
    workload_statistics.csv
    scalability_statistics.csv

-----------------------------------------------------------------------------
"""

from pathlib import Path
import pandas as pd
import numpy as np

RESULTS_DIR = Path("../results")

INPUT_FILE = RESULTS_DIR / "scalability_results.csv"


# --------------------------------------------------------------------------
# Dataset Loader
# --------------------------------------------------------------------------

def load_dataset():

    if not INPUT_FILE.exists():

        raise FileNotFoundError(

            f"Scalability benchmark not found: {INPUT_FILE}"

        )

    return pd.read_csv(INPUT_FILE)


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def validate_dataset(df):

    required = [

        "contract",

        "workload",

        "totalGas",

        "averageGas",

        "executionTimeMs",

        "throughput"

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
# Scalability Summary
# --------------------------------------------------------------------------

def scalability_summary(df):

    summary = (

        df.groupby("contract")

        .agg({

            "workload": "max",

            "averageGas": "mean",

            "executionTimeMs": "mean",

            "throughput": "mean"

        })

        .reset_index()

    )

    summary.columns = [

        "Contract",

        "MaximumWorkload",

        "AverageGas",

        "AverageLatency(ms)",

        "AverageTPS"

    ]

    summary.to_csv(

        RESULTS_DIR /

        "scalability_summary.csv",

        index=False

    )

    return summary


# --------------------------------------------------------------------------
# Throughput Analysis
# --------------------------------------------------------------------------

def throughput_analysis(df):

    throughput = (

        df.groupby([

            "contract",

            "workload"

        ])["throughput"]

        .mean()

        .reset_index()

    )

    throughput.columns = [

        "Contract",

        "Workload",

        "TransactionsPerSecond"

    ]

    throughput.to_csv(

        RESULTS_DIR /

        "throughput_results.csv",

        index=False

    )

    return throughput


# --------------------------------------------------------------------------
# Workload Growth
# --------------------------------------------------------------------------

def workload_statistics(df):

    records = []

    for contract in sorted(df["contract"].unique()):

        subset = df[

            df["contract"] == contract

        ]

        records.append({

            "Contract": contract,

            "MinimumWorkload":

                subset["workload"].min(),

            "MaximumWorkload":

                subset["workload"].max(),

            "AverageWorkload":

                round(

                    subset["workload"].mean(),

                    2

                ),

            "AverageExecutionTime(ms)":

                round(

                    subset["executionTimeMs"].mean(),

                    4

                )

        })

    workload_df = pd.DataFrame(records)

    workload_df.to_csv(

        RESULTS_DIR /

        "workload_statistics.csv",

        index=False

    )

    return workload_df


# --------------------------------------------------------------------------
# Scalability Metrics
# --------------------------------------------------------------------------

def scalability_metrics(df):

    baseline = (

        df[

            df["contract"] == "Baseline"

        ]["throughput"]

        .mean()

    )

    proposed = (

        df[

            df["contract"] == "Proposed"

        ]["throughput"]

        .mean()

    )

    improvement = (

        (proposed - baseline)

        /

        baseline

    ) * 100

    metrics = pd.DataFrame([{

        "BaselineTPS":

            round(baseline,2),

        "ProposedTPS":

            round(proposed,2),

        "ScalabilityImprovementPercent":

            round(improvement,2)

    }])

    metrics.to_csv(

        RESULTS_DIR /

        "scalability_statistics.csv",

        index=False

    )

    return metrics


# --------------------------------------------------------------------------
# Main Pipeline
# --------------------------------------------------------------------------

def run_scalability_analysis():

    print("\n====================================")

    print("Scalability Analysis")

    print("====================================")

    df = load_dataset()

    validate_dataset(df)

    summary = scalability_summary(df)

    throughput = throughput_analysis(df)

    workload = workload_statistics(df)

    metrics = scalability_metrics(df)

    print("\nScalability Summary")

    print(summary)

    print("\nThroughput")

    print(throughput)

    print("\nScalability Metrics")

    print(metrics)

    print("\nScalability analysis completed.\n")


if __name__ == "__main__":

    run_scalability_analysis()
