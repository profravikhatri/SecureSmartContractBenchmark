"""
-----------------------------------------------------------------------------
SecureSmartContractBenchmark

Module:
    Data Loading and Validation

Description:
    Loads benchmark results, validates dataset integrity,
    and performs preliminary quality checks before
    statistical analysis.

-----------------------------------------------------------------------------
"""

from pathlib import Path
import pandas as pd

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

RESULTS_DIR = Path("../results")

INPUT_FILE = RESULTS_DIR / "benchmark_results.csv"

REQUIRED_COLUMNS = [
    "contract",
    "iteration",
    "txHash",
    "blockNumber",
    "gasUsed",
    "latencyMs",
    "status"
]

# --------------------------------------------------------------------------
# Dataset Loader
# --------------------------------------------------------------------------

def load_dataset(file_path: Path) -> pd.DataFrame:
    """
    Load benchmark dataset from CSV.

    Parameters
    ----------
    file_path : Path
        Location of benchmark CSV file.

    Returns
    -------
    pandas.DataFrame
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Benchmark dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


# --------------------------------------------------------------------------
# Schema Validation
# --------------------------------------------------------------------------

def validate_schema(df: pd.DataFrame) -> None:
    """
    Verify that all required columns exist.
    """

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:

        raise ValueError(

            "Missing required columns:\n"

            + "\n".join(missing)

        )


# --------------------------------------------------------------------------
# Data Type Validation
# --------------------------------------------------------------------------

def validate_numeric_columns(df: pd.DataFrame) -> None:
    """
    Ensure numerical benchmark columns contain
    valid numeric values.
    """

    numeric_columns = [

        "iteration",

        "blockNumber",

        "gasUsed",

        "latencyMs",

        "status"

    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(

            df[column],

            errors="coerce"

        )

        if df[column].isnull().any():

            raise ValueError(

                f"Invalid numeric values detected "

                f"in column '{column}'."

            )


# --------------------------------------------------------------------------
# Missing Value Validation
# --------------------------------------------------------------------------

def check_missing_values(df: pd.DataFrame) -> int:
    """
    Count missing values.
    """

    return int(df.isnull().sum().sum())


# --------------------------------------------------------------------------
# Duplicate Record Validation
# --------------------------------------------------------------------------

def check_duplicates(df: pd.DataFrame) -> int:
    """
    Count duplicated benchmark rows.
    """

    return int(df.duplicated().sum())


# --------------------------------------------------------------------------
# Logical Validation
# --------------------------------------------------------------------------

def validate_business_rules(df: pd.DataFrame) -> None:
    """
    Validate benchmark values.
    """

    if (df["gasUsed"] <= 0).any():

        raise ValueError(

            "Gas usage must be greater than zero."

        )

    if (df["latencyMs"] <= 0).any():

        raise ValueError(

            "Latency must be greater than zero."

        )

    if (~df["status"].isin([0, 1])).any():

        raise ValueError(

            "Status column must contain only 0 or 1."

        )

    if df["txHash"].duplicated().any():

        raise ValueError(

            "Duplicate transaction hashes detected."

        )


# --------------------------------------------------------------------------
# Dataset Summary
# --------------------------------------------------------------------------

def dataset_summary(df: pd.DataFrame) -> dict:
    """
    Generate dataset summary.
    """

    return {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Contracts": df["contract"].nunique(),

        "Missing Values": check_missing_values(df),

        "Duplicate Rows": check_duplicates(df)

    }


# --------------------------------------------------------------------------
# Validation Pipeline
# --------------------------------------------------------------------------

def validate_dataset() -> pd.DataFrame:
    """
    Complete dataset validation workflow.
    """

    print("\n====================================")
    print("Dataset Validation")
    print("====================================")

    df = load_dataset(INPUT_FILE)

    validate_schema(df)

    validate_numeric_columns(df)

    validate_business_rules(df)

    summary = dataset_summary(df)

    print("\nDataset Summary")

    for key, value in summary.items():

        print(f"{key:20}: {value}")

    print("\nValidation completed successfully.\n")

    return df


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

if __name__ == "__main__":

    benchmark_data = validate_dataset()