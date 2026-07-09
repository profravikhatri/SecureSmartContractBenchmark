const { expect } = require("chai");
const { ethers } = require("hardhat");
const fs = require("fs");
const path = require("path");

describe("Scalability Benchmark", function () {

    let owner;
    let producer;
    let consumer;

    let oracle;
    let runtime;

    let framework;
    let baseline;

    const workloadSizes = [10, 25, 50, 100];

    const benchmarkResults = [];

    before(async function () {

        [owner, producer, consumer] =
            await ethers.getSigners();

        const OracleManager =
            await ethers.getContractFactory("OracleManager");

        oracle = await OracleManager.deploy();

        await oracle.waitForDeployment();

        await oracle.updateOracle(5);

        const RuntimeMonitor =
            await ethers.getContractFactory("RuntimeMonitor");

        runtime = await RuntimeMonitor.deploy();

        await runtime.waitForDeployment();

        const BaselineContract =
            await ethers.getContractFactory("BaselineContract");

        baseline = await BaselineContract.deploy();

        await baseline.waitForDeployment();

        const ProposedFramework =
            await ethers.getContractFactory("ProposedFramework");

        framework = await ProposedFramework.deploy(
            await oracle.getAddress(),
            await runtime.getAddress()
        );

        await framework.waitForDeployment();

        await framework.authorizeUser(
            producer.address
        );

    });

    async function executeWorkload(contract, contractName, size) {

        const start = process.hrtime.bigint();

        let totalGas = 0;

        for (let i = 0; i < size; i++) {

            let tx;

            if (contractName === "Baseline") {

                tx = await contract.recordTransaction(
                    consumer.address,
                    100 + i,
                    5
                );

            } else {

                tx = await contract
                    .connect(producer)
                    .createTransaction(
                        consumer.address,
                        100 + i,
                        5
                    );

            }

            const receipt = await tx.wait();

            totalGas += Number(receipt.gasUsed);

        }

        const end = process.hrtime.bigint();

        benchmarkResults.push({

            contract: contractName,

            workload: size,

            totalGas,

            averageGas:
                totalGas / size,

            executionTimeMs:
                Number(end - start) / 1e6,

            throughput:
                size /
                (Number(end - start) / 1e9)

        });

    }

    it("Should evaluate scalability", async function () {

        for (const size of workloadSizes) {

            await executeWorkload(
                baseline,
                "Baseline",
                size
            );

            await executeWorkload(
                framework,
                "Proposed",
                size
            );

        }

        expect(
            benchmarkResults.length
        ).to.equal(
            workloadSizes.length * 2
        );

    });

    after(function () {

        const outputDirectory =
            path.join(__dirname, "..", "results");

        if (!fs.existsSync(outputDirectory)) {

            fs.mkdirSync(outputDirectory);

        }

        fs.writeFileSync(

            path.join(
                outputDirectory,
                "scalability_results.json"
            ),

            JSON.stringify(
                benchmarkResults,
                null,
                4
            )

        );

    });

});