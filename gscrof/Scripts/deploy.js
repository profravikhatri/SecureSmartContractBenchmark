/**
 * --------------------------------------------------------------------------
 * SecureSmartContractBenchmark
 * --------------------------------------------------------------------------
 * Deployment Script
 *
 * Deploys the complete benchmark environment.
 *
 * Contracts
 * ----------
 * 1. BaselineContract
 * 2. AccessManager
 * 3. OracleManager
 * 4. RuntimeMonitor
 * 5. PerformanceValidation
 * 6. ProposedFramework
 * 7. ReentrancyValidation
 * 8. ReplayValidation
 * 9. AuthorizationValidation
 * 10. OracleValidation
 * --------------------------------------------------------------------------
 */

const hre = require("hardhat");

async function main() {

    console.log("\n========================================");
    console.log("SecureSmartContractBenchmark");
    console.log("Deployment Started");
    console.log("========================================\n");

    const [deployer] = await hre.ethers.getSigners();

    console.log("Deploying Account :", deployer.address);

    console.log(
        "Balance :",
        hre.ethers.formatEther(
            await hre.ethers.provider.getBalance(
                deployer.address
            )
        ),
        "ETH\n"
    );

    /*
    -------------------------------------------------------------------------
    Baseline Contract
    -------------------------------------------------------------------------
    */

    const BaselineContract =
        await hre.ethers.getContractFactory(
            "BaselineContract"
        );

    const baseline =
        await BaselineContract.deploy();

    await baseline.waitForDeployment();

    console.log(
        "BaselineContract :",
        await baseline.getAddress()
    );

    /*
    -------------------------------------------------------------------------
    Access Manager
    -------------------------------------------------------------------------
    */

    const AccessManager =
        await hre.ethers.getContractFactory(
            "AccessManager"
        );

    const access =
        await AccessManager.deploy();

    await access.waitForDeployment();

    console.log(
        "AccessManager :",
        await access.getAddress()
    );

    /*
    -------------------------------------------------------------------------
    Oracle Manager
    -------------------------------------------------------------------------
    */

    const OracleManager =
        await hre.ethers.getContractFactory(
            "OracleManager"
        );

    const oracle =
        await OracleManager.deploy();

    await oracle.waitForDeployment();

    console.log(
        "OracleManager :",
        await oracle.getAddress()
    );

    /*
    -------------------------------------------------------------------------
    Runtime Monitor
    -------------------------------------------------------------------------
    */

    const RuntimeMonitor =
        await hre.ethers.getContractFactory(
            "RuntimeMonitor"
        );

    const runtime =
        await RuntimeMonitor.deploy();

    await runtime.waitForDeployment();

    console.log(
        "RuntimeMonitor :",
        await runtime.getAddress()
    );

    /*
    -------------------------------------------------------------------------
    Performance Validation
    -------------------------------------------------------------------------
    */

    const PerformanceValidation =
        await hre.ethers.getContractFactory(
            "PerformanceValidation"
        );

    const performance =
        await PerformanceValidation.deploy();

    await performance.waitForDeployment();

    console.log(
        "PerformanceValidation :",
        await performance.getAddress()
    );

    /*
    -------------------------------------------------------------------------
    Proposed Framework
    -------------------------------------------------------------------------
    */

    const ProposedFramework =
        await hre.ethers.getContractFactory(
            "ProposedFramework"
        );

    const framework =
        await ProposedFramework.deploy(
            await oracle.getAddress(),
            await runtime.getAddress()
        );

    await framework.waitForDeployment();

    console.log(
        "ProposedFramework :",
        await framework.getAddress()
    );

    /*
    -------------------------------------------------------------------------
    Validation Contracts
    -------------------------------------------------------------------------
    */

    const ReentrancyValidation =
        await hre.ethers.getContractFactory(
            "ReentrancyValidation"
        );

    const reentrancy =
        await ReentrancyValidation.deploy(
            await framework.getAddress()
        );

    await reentrancy.waitForDeployment();

    console.log(
        "ReentrancyValidation :",
        await reentrancy.getAddress()
    );

    const ReplayValidation =
        await hre.ethers.getContractFactory(
            "ReplayValidation"
        );

    const replay =
        await ReplayValidation.deploy(
            await framework.getAddress()
        );

    await replay.waitForDeployment();

    console.log(
        "ReplayValidation :",
        await replay.getAddress()
    );

    const AuthorizationValidation =
        await hre.ethers.getContractFactory(
            "AuthorizationValidation"
        );

    const authorization =
        await AuthorizationValidation.deploy(
            await access.getAddress()
        );

    await authorization.waitForDeployment();

    console.log(
        "AuthorizationValidation :",
        await authorization.getAddress()
    );

    const OracleValidation =
        await hre.ethers.getContractFactory(
            "OracleValidation"
        );

    const oracleValidation =
        await OracleValidation.deploy(
            await oracle.getAddress()
        );

    await oracleValidation.waitForDeployment();

    console.log(
        "OracleValidation :",
        await oracleValidation.getAddress()
    );

    console.log("\n========================================");
    console.log("Deployment Completed Successfully");
    console.log("========================================\n");

}

main().catch((error) => {

    console.error(error);

    process.exitCode = 1;

});