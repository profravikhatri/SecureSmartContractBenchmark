/**
 * -----------------------------------------------------------------------------
 * SecureSmartContractBenchmark
 * -----------------------------------------------------------------------------
 * File : benchmark.js
 *
 * Description:
 * Executes benchmark experiments for the proposed framework and
 * baseline implementation. The script records gas consumption,
 * execution latency, throughput, and transaction success.
 *
 * Results are exported to the /results directory.
 * -----------------------------------------------------------------------------
 */

const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

const ITERATIONS = Number(process.env.BENCHMARK_RUNS || 30);

async function benchmarkTransaction(contract, contractName, iteration) {

    const accounts = await hre.ethers.getSigners();

    const consumer = accounts[1].address;

    const energy = 100 + iteration;

    const price = 8;

    const start = process.hrtime.bigint();

    const tx = await contract.createTransaction(
        consumer,
        energy,
        price
    );

    const receipt = await tx.wait();

    const end = process.hrtime.bigint();

    const latency =
        Number(end - start) / 1000000;

    return {

        contract: contractName,

        iteration,

        txHash: receipt.hash,

        blockNumber: receipt.blockNumber,

        gasUsed: receipt.gasUsed.toString(),

        latencyMs: latency.toFixed(3),

        status: receipt.status

    };

}

async function main() {

    console.log("\n=====================================");
    console.log(" SecureSmartContractBenchmark ");
    console.log(" Benchmark Execution Started ");
    console.log("=====================================\n");

    const baseline =
        await hre.ethers.getContract("BaselineContract");

    const proposed =
        await hre.ethers.getContract("ProposedFramework");

    const benchmarkResults = [];

    console.log("Running Baseline Benchmark...\n");

    for (let i = 1; i <= ITERATIONS; i++) {

        benchmarkResults.push(

            await benchmarkTransaction(
                baseline,
                "BaselineContract",
                i
            )

        );

    }

    console.log("Running Proposed Benchmark...\n");

    for (let i = 1; i <= ITERATIONS; i++) {

        benchmarkResults.push(

            await benchmarkTransaction(
                proposed,
                "ProposedFramework",
                i
            )

        );

    }

    const outputDirectory =
        path.join(__dirname, "..", "results");

    if (!fs.existsSync(outputDirectory)) {

        fs.mkdirSync(outputDirectory);

    }

    const outputFile =
        path.join(
            outputDirectory,
            "benchmark_results.json"
        );

    fs.writeFileSync(

        outputFile,

        JSON.stringify(
            benchmarkResults,
            null,
            4
        )

    );

    console.table(benchmarkResults);

    console.log("\nBenchmark completed successfully.");

    console.log("Results saved to:");

    console.log(outputFile);

}

main().catch((error) => {

    console.error(error);

    process.exit(1);

});