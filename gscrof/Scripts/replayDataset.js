/**
 * -----------------------------------------------------------------------------
 * SecureSmartContractBenchmark
 * -----------------------------------------------------------------------------
 * File : replayDataset.js
 *
 * Description:
 * Reads SmartGridTransactions.csv and replays each transaction
 * against the BaselineContract and ProposedFramework.
 *
 * Benchmark metrics are collected for later statistical analysis.
 * -----------------------------------------------------------------------------
 */

const hre = require("hardhat");
const fs = require("fs");
const path = require("path");
const csv = require("csv-parser");

const DATASET =
    process.env.DATASET_PATH ||
    "dataset/SmartGridTransactions.csv";

const OUTPUT =
    "results/replay_results.json";

async function replayTransaction(
    contract,
    contractName,
    row
) {

    const start = process.hrtime.bigint();

    const tx =
        await contract.createTransaction(

            row.consumer,

            Number(row.energyAmount),

            Number(row.unitPrice)

        );

    const receipt = await tx.wait();

    const end = process.hrtime.bigint();

    return {

        contract: contractName,

        transactionId: row.transactionId,

        gasUsed: receipt.gasUsed.toString(),

        latencyMs:

            Number(end - start) /

            1000000,

        blockNumber: receipt.blockNumber,

        status: receipt.status

    };

}

async function loadDataset() {

    return new Promise((resolve) => {

        const rows = [];

        fs.createReadStream(DATASET)

            .pipe(csv())

            .on("data", (row) => {

                rows.push(row);

            })

            .on("end", () => {

                resolve(rows);

            });

    });

}

async function main() {

    console.log("\nDataset Replay Started\n");

    const dataset = await loadDataset();

    const baseline =
        await hre.ethers.getContract(
            "BaselineContract"
        );

    const proposed =
        await hre.ethers.getContract(
            "ProposedFramework"
        );

    const results = [];

    for (const row of dataset) {

        results.push(

            await replayTransaction(

                baseline,

                "Baseline",

                row

            )

        );

        results.push(

            await replayTransaction(

                proposed,

                "Proposed",

                row

            )

        );

    }

    fs.writeFileSync(

        OUTPUT,

        JSON.stringify(

            results,

            null,

            4

        )

    );

    console.log(

        "Replay Completed"

    );

    console.log(

        "Transactions :", dataset.length

    );

    console.log(

        "Results Saved :", OUTPUT

    );

}

main().catch(console.error);