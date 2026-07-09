# --------------------------------------------------------------------------
# Research Validation Report
# --------------------------------------------------------------------------

from datetime import datetime


def generate_validation_report(
    dataset_summary: dict,
    outlier_summary: pd.DataFrame,
    normality_df: pd.DataFrame,
    confidence_df: pd.DataFrame,
    hypothesis_df: pd.DataFrame,
    effect_df: pd.DataFrame,
    output_directory: Path = RESULTS_DIR
) -> None:
    """
    Generate a comprehensive validation report summarizing
    the complete benchmark analysis.
    """

    report_file = output_directory / "validation_report.txt"

    with open(report_file, "w", encoding="utf-8") as report:

        report.write("=" * 72 + "\n")
        report.write("SecureSmartContractBenchmark\n")
        report.write("Research Validation Report\n")
        report.write("=" * 72 + "\n\n")

        report.write(
            f"Generated : {datetime.now()}\n\n"
        )

        report.write("1. Dataset Summary\n")
        report.write("-" * 40 + "\n")

        for key, value in dataset_summary.items():
            report.write(f"{key:25}: {value}\n")

        report.write("\n")

        report.write("2. Outlier Analysis\n")
        report.write("-" * 40 + "\n")

        report.write(
            outlier_summary.to_string(index=False)
        )

        report.write("\n\n")

        report.write("3. Normality Assessment\n")
        report.write("-" * 40 + "\n")

        report.write(
            normality_df.to_string(index=False)
        )

        report.write("\n\n")

        report.write("4. Confidence Intervals\n")
        report.write("-" * 40 + "\n")

        report.write(
            confidence_df.to_string(index=False)
        )

        report.write("\n\n")

        report.write("5. Hypothesis Testing\n")
        report.write("-" * 40 + "\n")

        report.write(
            hypothesis_df.to_string(index=False)
        )

        report.write("\n\n")

        report.write("6. Effect Size Analysis\n")
        report.write("-" * 40 + "\n")

        report.write(
            effect_df.to_string(index=False)
        )

        report.write("\n\n")

        report.write("7. Overall Validation Status\n")
        report.write("-" * 40 + "\n")

        significant = (
            hypothesis_df["Significant"] == "Yes"
        ).all()

        if significant:
            report.write(
                "Statistical testing indicates significant "
                "differences between the baseline and the "
                "proposed framework.\n"
            )
        else:
            report.write(
                "No statistically significant difference "
                "was detected for one or more benchmark metrics.\n"
            )

        report.write(
            "\nThe benchmark pipeline completed successfully.\n"
        )

        report.write(
            "All analyses were performed using reproducible "
            "statistical procedures.\n"
        )

    print("\n====================================")
    print("Validation Report Generated")
    print("====================================")
    print(f"\nReport saved to: {report_file}")