const { expect } = require("chai");
const { ethers } = require("hardhat");
const fs = require("fs");
const path = require("path");

describe("Performance Benchmark", function () {

    let owner;
    let producer;
    let consumer;

    let oracle;
    let runtime;
    let framework;

    const ITERATIONS = 30;
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

    it("Should execute benchmark iterations", async function () {

        for (let i = 1; i <= ITERATIONS; i++) {

            const start =
                process.hrtime.bigint();

            const tx =
                await framework.connect(producer)
                    .createTransaction(
                        consumer.address,
                        100 + i,
                        5
                    );

            const receipt =
                await tx.wait();

            const end =
                process.hrtime.bigint();

            benchmarkResults.push({

                iteration: i,

                gasUsed:
                    Number(receipt.gasUsed),

                executionTimeMs:
                    Number(end - start) / 1e6,

                blockNumber:
                    receipt.blockNumber,

                status:
                    receipt.status

            });

        }

        expect(
            benchmarkResults.length
        ).to.equal(ITERATIONS);

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
                "performance_results.json"
            ),

            JSON.stringify(
                benchmarkResults,
                null,
                4
            )

        );

    });

});