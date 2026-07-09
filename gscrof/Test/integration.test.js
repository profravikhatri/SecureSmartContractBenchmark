const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("End-to-End Integration Test", function () {

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

    it("Should complete full transaction lifecycle", async function () {

        await framework.connect(producer).createTransaction(

            consumer.address,

            100,

            5

        );

        expect(

            await framework.totalTransactions()

        ).to.equal(1);

        await framework.verifyTransaction(1);

        let transaction =

            await framework.getTransaction(1);

        expect(

            transaction.verified

        ).to.equal(true);

        await framework.completeTransaction(1);

        transaction =

            await framework.getTransaction(1);

        expect(

            transaction.completed

        ).to.equal(true);

    });

    it("Should maintain sequential nonce values", async function () {

        for(let i = 0; i < 5; i++){

            await framework.connect(producer).createTransaction(

                consumer.address,

                100 + i,

                5

            );

        }

        expect(

            await framework.accountNonce(

                producer.address

            )

        ).to.equal(5);

    });

    it("Should reject unauthorized participant", async function () {

        await expect(

            framework.connect(consumer).createTransaction(

                owner.address,

                50,

                5

            )

        ).to.be.reverted;

    });

});