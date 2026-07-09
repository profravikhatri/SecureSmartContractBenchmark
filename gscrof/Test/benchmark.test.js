const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Benchmark Comparison", function () {

    let owner;
    let consumer;

    let oracle;
    let runtime;

    let baseline;
    let proposed;

    beforeEach(async function () {

        [owner, consumer] = await ethers.getSigners();

        const OracleManager =
            await ethers.getContractFactory("OracleManager");

        oracle = await OracleManager.deploy();

        await oracle.waitForDeployment();

        const RuntimeMonitor =
            await ethers.getContractFactory("RuntimeMonitor");

        runtime = await RuntimeMonitor.deploy();

        await runtime.waitForDeployment();

        const Baseline =
            await ethers.getContractFactory("BaselineContract");

        baseline = await Baseline.deploy();

        await baseline.waitForDeployment();

        const Proposed =
            await ethers.getContractFactory("ProposedFramework");

        proposed = await Proposed.deploy(

            await oracle.getAddress(),

            await runtime.getAddress()

        );

        await proposed.waitForDeployment();

    });

    it("Should deploy both contracts", async function () {

        expect(

            await baseline.totalTransactions()

        ).to.equal(0);

        expect(

            await proposed.totalTransactions()

        ).to.equal(0);

    });

    it("Should execute baseline transaction", async function () {

        await baseline.recordTransaction(

            consumer.address,

            100,

            5

        );

        expect(

            await baseline.totalTransactions()

        ).to.equal(1);

    });

    it("Should execute proposed transaction", async function () {

        await proposed.authorizeUser(

            owner.address

        );

        await oracle.updateOracle(5);

        await proposed.createTransaction(

            consumer.address,

            100,

            5

        );

        expect(

            await proposed.totalTransactions()

        ).to.equal(1);

    });

    it("Should compare gas consumption", async function () {

        const tx1 =

            await baseline.recordTransaction(

                consumer.address,

                100,

                5

            );

        const receipt1 =

            await tx1.wait();

        await oracle.updateOracle(5);

        const tx2 =

            await proposed.createTransaction(

                consumer.address,

                100,

                5

            );

        const receipt2 =

            await tx2.wait();

        console.log(

            "\nBaseline Gas :",

            receipt1.gasUsed.toString()

        );

        console.log(

            "Proposed Gas :",

            receipt2.gasUsed.toString()

        );

        expect(

            receipt1.gasUsed

        ).to.be.gt(0);

        expect(

            receipt2.gasUsed

        ).to.be.gt(0);

    });

});