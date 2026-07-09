# --------------------------------------------------------------------------
# Main Execution Pipeline
# --------------------------------------------------------------------------

import logging
import traceback
from datetime import datetime


# --------------------------------------------------------------------------
# Configure Logger
# --------------------------------------------------------------------------

LOG_FILE = RESULTS_DIR / "analysis.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)


# --------------------------------------------------------------------------
# Analysis Pipeline
# --------------------------------------------------------------------------

def run_analysis_pipeline() -> bool:
    """
    Execute the complete statistical analysis workflow.

    Returns
    -------
    bool
        True if analysis completed successfully,
        otherwise False.
    """

    logging.info("=" * 70)
    logging.info("SecureSmartContractBenchmark")
    logging.info("Statistical Analysis Pipeline")
    logging.info("=" * 70)

    start_time = datetime.now()

    try:

        # --------------------------------------------------------------
        # Dataset Validation
        # --------------------------------------------------------------

        logging.info("Loading and validating dataset...")

        benchmark_data = validate_dataset()

        dataset_info = dataset_summary(
            benchmark_data
        )

        # --------------------------------------------------------------
        # Descriptive Statistics
        # --------------------------------------------------------------

        logging.info(
            "Computing descriptive statistics..."
        )

        descriptive_df = descriptive_statistics(
            benchmark_data
        )

        # --------------------------------------------------------------
        # Outlier Detection
        # --------------------------------------------------------------

        logging.info(
            "Detecting outliers..."
        )

        detect_outliers(
            benchmark_data
        )

        outlier_summary = pd.read_csv(
            RESULTS_DIR / "outlier_summary.csv"
        )

        # --------------------------------------------------------------
        # Normality Testing
        # --------------------------------------------------------------

        logging.info(
            "Performing normality testing..."
        )

        normality_df = normality_test(
            benchmark_data
        )

        # --------------------------------------------------------------
        # Confidence Intervals
        # --------------------------------------------------------------

        logging.info(
            "Computing confidence intervals..."
        )

        confidence_df = confidence_intervals(
            benchmark_data
        )

        # --------------------------------------------------------------
        # Hypothesis Testing
        # --------------------------------------------------------------

        logging.info(
            "Running hypothesis tests..."
        )

        hypothesis_df = hypothesis_testing(
            benchmark_data,
            normality_df
        )

        # --------------------------------------------------------------
        # Effect Size
        # --------------------------------------------------------------

        logging.info(
            "Computing effect sizes..."
        )

        effect_df = effect_size_analysis(
            benchmark_data,
            normality_df
        )

        # --------------------------------------------------------------
        # Summary Export
        # --------------------------------------------------------------

        logging.info(
            "Exporting summary statistics..."
        )

        export_summary_statistics(
            descriptive_df,
            confidence_df,
            hypothesis_df,
            effect_df
        )

        # --------------------------------------------------------------
        # Validation Report
        # --------------------------------------------------------------

        logging.info(
            "Generating validation report..."
        )

        generate_validation_report(
            dataset_info,
            outlier_summary,
            normality_df,
            confidence_df,
            hypothesis_df,
            effect_df
        )

        end_time = datetime.now()

        elapsed = end_time - start_time

        logging.info("=" * 70)
        logging.info("Analysis completed successfully.")
        logging.info(f"Execution Time : {elapsed}")
        logging.info("=" * 70)

        return True

    except Exception as exception:

        logging.error(
            "Analysis failed."
        )

        logging.error(str(exception))

        logging.error(
            traceback.format_exc()
        )

        return False


# --------------------------------------------------------------------------
# Entry Point
# --------------------------------------------------------------------------

if __name__ == "__main__":

    success = run_analysis_pipeline()

    if success:

        print("\nAnalysis completed successfully.\n")

    else:

        print("\nAnalysis terminated with errors.\n")