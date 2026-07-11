#!/usr/bin/env node

/**
 * SecureSmartContractBenchmark
 * Master Experiment Runner
 *
 * Author: Ravi Khatri
 */

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const RESULTS = path.join(ROOT, "results");
const LOGS = path.join(RESULTS, "logs");

if (!fs.existsSync(RESULTS))
    fs.mkdirSync(RESULTS);

if (!fs.existsSync(LOGS))
    fs.mkdirSync(LOGS);

const LOGFILE = path.join(
    LOGS,
    `experiment_${new Date()
        .toISOString()
        .replace(/:/g, "-")}.log`
);

function log(message) {

    console.log(message);

    fs.appendFileSync(
        LOGFILE,
        message + "\n"
    );

}

function execute(command, title) {

    log("\n=================================================");
    log(title);
    log("=================================================\n");

    try {

        execSync(command, {
            stdio: "inherit",
            cwd: ROOT
        });

        log("\nSUCCESS\n");

    }
    catch (err) {

        log("\nFAILED\n");
        process.exit(1);

    }

}

log("Secure Smart Contract Benchmark");
log("Started : " + new Date());

/*
----------------------------------------------------
Compile Contracts
----------------------------------------------------
*/

execute(
    "npx hardhat compile",
    "Compiling Smart Contracts"
);

/*
----------------------------------------------------
Deploy
----------------------------------------------------
*/

execute(
    "node scripts/deploy.js",
    "Deploying Contracts"
);

/*
----------------------------------------------------
Run Unit Tests
----------------------------------------------------
*/

execute(
    "npx hardhat test",
    "Running Unit Tests"
);

/*
----------------------------------------------------
Security Tests
----------------------------------------------------
*/

execute(
    "npx hardhat test test/security.test.js",
    "Security Evaluation"
);

/*
----------------------------------------------------
Attack Simulation
----------------------------------------------------
*/

execute(
    "npx hardhat test test/attacks.test.js",
    "Attack Simulation"
);

/*
----------------------------------------------------
Performance
----------------------------------------------------
*/

execute(
    "npx hardhat test test/performance.test.js",
    "Performance Evaluation"
);

/*
----------------------------------------------------
Scalability
----------------------------------------------------
*/

execute(
    "npx hardhat test test/scalability.test.js",
    "Scalability Evaluation"
);

/*
----------------------------------------------------
Oracle Evaluation
----------------------------------------------------
*/

execute(
    "npx hardhat test test/oracle.test.js",
    "Oracle Benchmark"
);

/*
----------------------------------------------------
Replay Dataset
----------------------------------------------------
*/

execute(
    "node scripts/replayDataset.js",
    "Dataset Replay"
);

/*
----------------------------------------------------
Run Benchmark
----------------------------------------------------
*/

execute(
    "node scripts/benchmark.js",
    "Benchmark Execution"
);

/*
----------------------------------------------------
Export Metrics
----------------------------------------------------
*/

execute(
    "node scripts/exportMetrics.js",
    "Export Benchmark Metrics"
);

/*
----------------------------------------------------
Python Analysis
----------------------------------------------------
*/

execute(
    "python analysis/statistics.py",
    "Statistical Analysis"
);

execute(
    "python analysis/gas_analysis.py",
    "Gas Analysis"
);

execute(
    "python analysis/latency_analysis.py",
    "Latency Analysis"
);

execute(
    "python analysis/security_analysis.py",
    "Security Analysis"
);

execute(
    "python analysis/scalability_analysis.py",
    "Scalability Analysis"
);

/*
----------------------------------------------------
Generate Figures
----------------------------------------------------
*/

execute(
    "python analysis/generate_figures.py",
    "Generate Publication Figures"
);

log("\n======================================");
log("ALL EXPERIMENTS COMPLETED");
log("======================================");

log("Finished : " + new Date());

console.log("\nResults saved inside:");
console.log("results/");
console.log("results/logs/");
