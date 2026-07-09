// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "./AccessManager.sol";
import "./OracleManager.sol";
import "./RuntimeMonitor.sol";
import "./libraries/SecurityLibrary.sol";
import "./libraries/OptimizationLibrary.sol";

contract ProposedFramework is AccessManager {

    using SecurityLibrary for uint256;
    using OptimizationLibrary for uint256;

    struct EnergyTransaction {

        uint256 id;

        address producer;

        address consumer;

        uint256 energyAmount;

        uint256 unitPrice;

        uint256 totalCost;

        uint256 timestamp;

        uint256 nonce;

        bool verified;

        bool completed;

    }

    mapping(uint256 => EnergyTransaction) private transactions;

    mapping(address => uint256) public accountNonce;

    uint256 public transactionCounter;

    OracleManager public oracle;

    RuntimeMonitor public runtimeMonitor;

    event TransactionCreated(

        uint256 indexed id,

        address indexed producer,

        address indexed consumer,

        uint256 totalCost

    );

    event TransactionVerified(

        uint256 indexed id

    );

    event TransactionCompleted(

        uint256 indexed id

    );

    constructor(

        address oracleAddress,

        address runtimeAddress

    ) {

        oracle = OracleManager(oracleAddress);

        runtimeMonitor = RuntimeMonitor(runtimeAddress);

    }

    function createTransaction(

        address consumer,

        uint256 energyAmount,

        uint256 unitPrice

    )

        external

        onlyAuthorized

    {

        uint256 nonce = ++accountNonce[msg.sender];

        transactionCounter++;

        uint256 totalCost =

            energyAmount.calculateTotal(unitPrice);

        transactions[transactionCounter] =

            EnergyTransaction({

                id: transactionCounter,

                producer: msg.sender,

                consumer: consumer,

                energyAmount: energyAmount,

                unitPrice: unitPrice,

                totalCost: totalCost,

                timestamp: block.timestamp,

                nonce: nonce,

                verified: false,

                completed: false

            });

        runtimeMonitor.recordExecution(

            gasleft(),

            true

        );

        emit TransactionCreated(

            transactionCounter,

            msg.sender,

            consumer,

            totalCost

        );

    }

    function verifyTransaction(

        uint256 transactionId

    )

        external

        onlyAuthorized

    {

        EnergyTransaction storage txn =

            transactions[transactionId];

        require(

            !txn.verified,

            "Already verified"

        );

        require(

            oracle.validateEnergyRecord(

                txn.energyAmount,

                txn.totalCost

            ),

            "Oracle validation failed"

        );

        txn.verified = true;

        runtimeMonitor.recordExecution(

            gasleft(),

            true

        );

        emit TransactionVerified(

            transactionId

        );

    }

    function completeTransaction(

        uint256 transactionId

    )

        external

        onlyAuthorized

    {

        EnergyTransaction storage txn =

            transactions[transactionId];

        require(

            txn.verified,

            "Transaction not verified"

        );

        require(

            !txn.completed,

            "Already completed"

        );

        txn.completed = true;

        runtimeMonitor.recordExecution(

            gasleft(),

            true

        );

        emit TransactionCompleted(

            transactionId

        );

    }

    function getTransaction(

        uint256 transactionId

    )

        external

        view

        returns (

            EnergyTransaction memory

        )

    {

        return transactions[transactionId];

    }

    function totalTransactions()

        external

        view

        returns(uint256)

    {

        return transactionCounter;

    }

}