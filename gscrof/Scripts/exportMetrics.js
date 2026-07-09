/**
 * -----------------------------------------------------------------------------
 * SecureSmartContractBenchmark
 * -----------------------------------------------------------------------------
 * File : exportMetrics.js
 *
 * Description:
 * Converts benchmark JSON outputs into CSV files suitable for
 * statistical analysis, visualization, and publication.
 *
 * -----------------------------------------------------------------------------
 */

const fs = require("fs");
const path = require("path");

/* -------------------------------------------------------------------------- */
/* Configuration                                                              */
/* -------------------------------------------------------------------------- */

const INPUT_FILE =
    path.join(__dirname, "..", "results", "benchmark_results.json");

const OUTPUT_FILE =
    path.join(__dirname, "..", "results", "benchmark_results.csv");

/* -------------------------------------------------------------------------- */
/* JSON to CSV Conversion                                                     */
/* -------------------------------------------------------------------------- */

function convertToCSV(data) {

    if (data.length === 0) {

        return "";

    }

    const headers = Object.keys(data[0]);

    const csvRows = [];

    csvRows.push(headers.join(","));

    for (const row of data) {

        csvRows.push(

            headers

                .map(field => row[field])

                .join(",")

        );

    }

    return csvRows.join("\n");

}

/* -------------------------------------------------------------------------- */
/* Export Metrics                                                             */
/* -------------------------------------------------------------------------- */

function exportMetrics() {

    console.log("\n====================================");

    console.log("Exporting Benchmark Metrics");

    console.log("====================================\n");

    if (!fs.existsSync(INPUT_FILE)) {

        console.error(

            "Benchmark file not found."

        );

        process.exit(1);

    }

    const benchmarkData = JSON.parse(

        fs.readFileSync(

            INPUT_FILE,

            "utf8"

        )

    );

    const csv = convertToCSV(

        benchmarkData

    );

    fs.writeFileSync(

        OUTPUT_FILE,

        csv

    );

    console.log(

        "Benchmark Records :",

        benchmarkData.length

    );

    console.log(

        "CSV Export :", OUTPUT_FILE

    );

}

/* -------------------------------------------------------------------------- */

exportMetrics();