const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Oracle Validation Tests", function () {

    let owner;
    let producer;
    let consumer;

    let oracle;
    let runtime;
    let framework;

    beforeEach(async function () {

        [owner, producer, consumer] =
            await ethers.getSigners();

        const OracleManager =
            await ethers.getContractFactory("OracleManager");

        oracle = await OracleManager.deploy();

        await oracle.waitForDeployment();

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

    /* ----------------------------------------------------- */

    it("Should update oracle price", async function () {

        await oracle.updateOracle(5);

        expect(

            await oracle.getLatestPrice()

        ).to.equal(5);

    });

    /* ----------------------------------------------------- */

    it("Should validate oracle timestamp", async function () {

        await oracle.updateOracle(8);

        const lastUpdate =

            await oracle.getLastUpdate();

        expect(lastUpdate).to.be.gt(0);

    });

    /* ----------------------------------------------------- */

    it("Should verify transaction with valid oracle data", async function () {

        await oracle.updateOracle(5);

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

    /* ----------------------------------------------------- */

    it("Should reject transaction when oracle price is unavailable", async function () {

        await framework.connect(producer).createTransaction(

            consumer.address,

            100,

            5

        );

        await expect(

            framework.verifyTransaction(1)

        ).to.be.reverted;

    });

    /* ----------------------------------------------------- */

    it("Should reject incorrect transaction values", async function () {

        await oracle.updateOracle(10);

        await framework.connect(producer).createTransaction(

            consumer.address,

            100,

            5

        );

        await expect(

            framework.verifyTransaction(1)

        ).to.be.reverted;

    });

    /* ----------------------------------------------------- */

    it("Should expose oracle benchmark information", async function () {

        await oracle.updateOracle(7);

        expect(

            await oracle.totalOracleRecords()

        ).to.equal(1);

    });

});