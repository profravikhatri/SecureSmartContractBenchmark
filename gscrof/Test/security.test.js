const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Security Validation", function () {

    let owner;
    let producer;
    let consumer;
    let outsider;

    let oracle;
    let runtime;
    let framework;

    beforeEach(async function () {

        [owner, producer, consumer, outsider] =
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

        await framework.authorizeUser(producer.address);

    });

    /* ------------------------------------------------------ */

    it("Should reject unauthorized transaction creation", async function () {

        await expect(

            framework.connect(outsider).createTransaction(

                consumer.address,
                100,
                5

            )

        ).to.be.reverted;

    });

    /* ------------------------------------------------------ */

    it("Should allow authorized participant", async function () {

        await framework.connect(producer).createTransaction(

            consumer.address,
            100,
            5

        );

        expect(

            await framework.totalTransactions()

        ).to.equal(1);

    });

    /* ------------------------------------------------------ */

    it("Should assign sequential nonces", async function () {

        await framework.connect(producer).createTransaction(

            consumer.address,
            100,
            5

        );

        expect(

            await framework.accountNonce(

                producer.address

            )

        ).to.equal(1);

    });

    /* ------------------------------------------------------ */

    it("Should verify oracle data", async function () {

        await framework.connect(producer).createTransaction(

            consumer.address,
            100,
            5

        );

        await framework.verifyTransaction(1);

        const txData =

            await framework.getTransaction(1);

        expect(

            txData.verified

        ).to.equal(true);

    });

    /* ------------------------------------------------------ */

    it("Should complete verified transaction", async function () {

        await framework.connect(producer).createTransaction(

            consumer.address,
            100,
            5

        );

        await framework.verifyTransaction(1);

        await framework.completeTransaction(1);

        const txData =

            await framework.getTransaction(1);

        expect(

            txData.completed

        ).to.equal(true);

    });

    /* ------------------------------------------------------ */

    it("Should reject duplicate completion", async function () {

        await framework.connect(producer).createTransaction(

            consumer.address,
            100,
            5

        );

        await framework.verifyTransaction(1);

        await framework.completeTransaction(1);

        await expect(

            framework.completeTransaction(1)

        ).to.be.reverted;

    });

});