 SPDX-License-Identifier MIT

pragma solidity ^0.8.28;


  ------------------------------------------------------------------------
  SecureSmartContractBenchmark
  ------------------------------------------------------------------------
  Contract Name  BaselineContract
 
  Description
  A conventional smart contract for recording decentralized
  energy transactions without additional optimization or
  security enhancements.
 
  This contract serves as the baseline implementation for
  benchmarking computational cost, execution latency,
  and scalability against the proposed framework.
 
  ------------------------------------------------------------------------
 

contract BaselineContract {

    struct EnergyTransaction {

        uint256 transactionId;

        address producer;

        address consumer;

        uint256 energyAmount;

        uint256 unitPrice;

        uint256 totalCost;

        uint256 timestamp;

    }

    uint256 public transactionCounter;

    mapping(uint256 = EnergyTransaction) private transactions;

    event TransactionRecorded(

        uint256 indexed transactionId,

        address indexed producer,

        address indexed consumer,

        uint256 energyAmount,

        uint256 totalCost

    );

    event TransactionUpdated(

        uint256 indexed transactionId

    );

    event TransactionDeleted(

        uint256 indexed transactionId

    );

    
      --------------------------------------------------------
      Record Energy Transaction
      --------------------------------------------------------
     

    function recordTransaction(

        address consumer,

        uint256 energyAmount,

        uint256 unitPrice

    )

        external

    {

        transactionCounter++;

        uint256 totalCost = energyAmount  unitPrice;

        transactions[transactionCounter] = EnergyTransaction({

            transactionId transactionCounter,

            producer msg.sender,

            consumer consumer,

            energyAmount energyAmount,

            unitPrice unitPrice,

            totalCost totalCost,

            timestamp block.timestamp

        });

        emit TransactionRecorded(

            transactionCounter,

            msg.sender,

            consumer,

            energyAmount,

            totalCost

        );

    }

    
      --------------------------------------------------------
      Read Transaction
      --------------------------------------------------------
     

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

    
      --------------------------------------------------------
      Update Transaction
      --------------------------------------------------------
     

    function updateTransaction(

        uint256 transactionId,

        uint256 energyAmount,

        uint256 unitPrice

    )

        external

    {

        EnergyTransaction storage txData =

            transactions[transactionId];

        txData.energyAmount = energyAmount;

        txData.unitPrice = unitPrice;

        txData.totalCost = energyAmount  unitPrice;

        emit TransactionUpdated(

            transactionId

        );

    }

    
      --------------------------------------------------------
      Delete Transaction
      --------------------------------------------------------
     

    function deleteTransaction(

        uint256 transactionId

    )

        external

    {

        delete transactions[transactionId];

        emit TransactionDeleted(

            transactionId

        );

    }

    
      --------------------------------------------------------
      Total Transactions
      --------------------------------------------------------
     

    function totalTransactions()

        external

        view

        returns (uint256)

    {

        return transactionCounter;

    }

}