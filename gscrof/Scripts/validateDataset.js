#!/usr/bin/env node

/**
 * SecureSmartContractBenchmark
 * Dataset Validation Script
 *
 * Usage:
 * node scripts/validateDataset.js dataset/SmartGridTransactions.csv
 */

const fs = require("fs");
const path = require("path");
const csv = require("csv-parser");

const inputFile =
    process.argv[2] ||
    "dataset/SmartGridTransactions.csv";

const REQUIRED_COLUMNS = [
    "transaction_id",
    "timestamp",
    "sender",
    "receiver",
    "energy_kwh",
    "gas_used",
    "latency_ms",
    "block_number",
    "consensus",
    "attack_type",
    "status"
];

const ETH_REGEX = /^0x[a-fA-F0-9]{40}$/;
const HASH_REGEX = /^0x[a-fA-F0-9]{64}$/;

const report = {
    file: inputFile,
    rows: 0,
    passed: true,
    missingColumns: [],
    duplicateRows: 0,
    missingValues: 0,
    invalidAddresses: 0,
    invalidHashes: 0,
    invalidTimestamp: 0,
    invalidEnergy: 0,
    invalidLatency: 0,
    invalidGas: 0,
    invalidBlock: 0,
    warnings: [],
    errors: []
};

const rows = [];
const uniqueTransactions = new Set();

if (!fs.existsSync(inputFile)) {

    console.error("Dataset not found.");
    process.exit(1);

}

fs.createReadStream(inputFile)
.pipe(csv())
.on("headers", headers => {

    REQUIRED_COLUMNS.forEach(col => {

        if (!headers.includes(col))
            report.missingColumns.push(col);

    });

})
.on("data", row => {

    report.rows++;

    rows.push(row);

    Object.keys(row).forEach(k => {

        if (
            row[k] === undefined ||
            row[k] === null ||
            row[k].toString().trim() === ""
        )
            report.missingValues++;

    });

    if (uniqueTransactions.has(row.transaction_id))
        report.duplicateRows++;

    uniqueTransactions.add(row.transaction_id);

    if (
        row.sender &&
        !ETH_REGEX.test(row.sender)
    )
        report.invalidAddresses++;

    if (
        row.receiver &&
        !ETH_REGEX.test(row.receiver)
    )
        report.invalidAddresses++;

    if (
        row.transaction_id &&
        !HASH_REGEX.test(row.transaction_id)
    )
        report.invalidHashes++;

    if (
        isNaN(Date.parse(row.timestamp))
    )
        report.invalidTimestamp++;

    if (
        Number(row.energy_kwh) < 0
    )
        report.invalidEnergy++;

    if (
        Number(row.latency_ms) < 0
    )
        report.invalidLatency++;

    if (
        Number(row.gas_used) < 0
    )
        report.invalidGas++;

    if (
        Number(row.block_number) < 0
    )
        report.invalidBlock++;

})
.on("end", () => {

    if (report.rows === 0)
        report.errors.push("Dataset is empty.");

    if (report.missingColumns.length > 0)
        report.errors.push("Required columns missing.");

    if (report.invalidAddresses > 0)
        report.errors.push("Invalid Ethereum addresses detected.");

    if (report.invalidHashes > 0)
        report.errors.push("Invalid transaction hashes detected.");

    if (report.invalidTimestamp > 0)
        report.errors.push("Invalid timestamps detected.");

    if (report.invalidEnergy > 0)
        report.errors.push("Negative energy values.");

    if (report.invalidGas > 0)
        report.errors.push("Negative gas values.");

    if (report.invalidLatency > 0)
        report.errors.push("Negative latency values.");

    if (report.invalidBlock > 0)
        report.errors.push("Negative block numbers.");

    if (report.duplicateRows > 0)
        report.warnings.push("Duplicate transaction IDs.");

    if (report.missingValues > 0)
        report.warnings.push("Missing values detected.");

    report.passed = report.errors.length === 0;

    if (!fs.existsSync("results"))
        fs.mkdirSync("results");

    fs.writeFileSync(
        "results/dataset_validation_report.json",
        JSON.stringify(report, null, 4)
    );

    const csvReport = [
        "Metric,Value",
        `Rows,${report.rows}`,
        `Missing Columns,${report.missingColumns.length}`,
        `Duplicate Rows,${report.duplicateRows}`,
        `Missing Values,${report.missingValues}`,
        `Invalid Addresses,${report.invalidAddresses}`,
        `Invalid Hashes,${report.invalidHashes}`,
        `Invalid Timestamp,${report.invalidTimestamp}`,
        `Invalid Energy,${report.invalidEnergy}`,
        `Invalid Latency,${report.invalidLatency}`,
        `Invalid Gas,${report.invalidGas}`,
        `Invalid Block,${report.invalidBlock}`,
        `Validation Passed,${report.passed}`
    ];

    fs.writeFileSync(
        "results/dataset_validation_summary.csv",
        csvReport.join("\n")
    );

    console.log("\n================================");
    console.log("DATASET VALIDATION REPORT");
    console.log("================================");

    console.table({
        Rows: report.rows,
        Passed: report.passed,
        MissingColumns: report.missingColumns.length,
        MissingValues: report.missingValues,
        DuplicateRows: report.duplicateRows,
        InvalidAddresses: report.invalidAddresses,
        InvalidHashes: report.invalidHashes,
        InvalidTimestamp: report.invalidTimestamp,
        InvalidEnergy: report.invalidEnergy,
        InvalidLatency: report.invalidLatency,
        InvalidGas: report.invalidGas,
        InvalidBlock: report.invalidBlock
    });

    console.log("\nJSON Report:");
    console.log("results/dataset_validation_report.json");

    console.log("CSV Summary:");
    console.log("results/dataset_validation_summary.csv");

    if (!report.passed)
        process.exit(1);

});
