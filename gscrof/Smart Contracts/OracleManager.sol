// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

/**
 * -----------------------------------------------------------------------------
 * SecureSmartContractBenchmark
 * -----------------------------------------------------------------------------
 * Contract : OracleManager
 *
 * Description:
 * Lightweight oracle validation contract for benchmark experiments.
 * It validates external energy records before they are accepted by
 * the proposed framework.
 *
 * This contract is designed for reproducible benchmarking and should
 * not be considered a production oracle implementation.
 * -----------------------------------------------------------------------------
 */

contract OracleManager {

    /// Contract administrator
    address public owner;

    /// Latest approved energy price
    uint256 public latestEnergyPrice;

    /// Last oracle update
    uint256 public lastUpdated;

    /// Oracle freshness interval
    uint256 public constant MAX_DATA_AGE = 3600;

    struct OracleRecord {

        uint256 energyPrice;

        uint256 timestamp;

        bool valid;

    }

    mapping(uint256 => OracleRecord) public records;

    uint256 public recordCounter;

    /* ---------------------------------------------------------------------- */
    /* Events                                                                 */
    /* ---------------------------------------------------------------------- */

    event OracleUpdated(

        uint256 indexed recordId,

        uint256 energyPrice,

        uint256 timestamp

    );

    event OracleValidation(

        uint256 indexed energyAmount,

        uint256 totalCost,

        bool status

    );

    /* ---------------------------------------------------------------------- */
    /* Modifiers                                                              */
    /* ---------------------------------------------------------------------- */

    modifier onlyOwner() {

        require(

            msg.sender == owner,

            "OracleManager: owner only"

        );

        _;

    }

    /* ---------------------------------------------------------------------- */
    /* Constructor                                                            */
    /* ---------------------------------------------------------------------- */

    constructor() {

        owner = msg.sender;

    }

    /* ---------------------------------------------------------------------- */
    /* Oracle Update                                                          */
    /* ---------------------------------------------------------------------- */

    function updateOracle(

        uint256 energyPrice

    )

        external

        onlyOwner

    {

        require(

            energyPrice > 0,

            "OracleManager: invalid price"

        );

        latestEnergyPrice = energyPrice;

        lastUpdated = block.timestamp;

        recordCounter++;

        records[recordCounter] = OracleRecord({

            energyPrice: energyPrice,

            timestamp: block.timestamp,

            valid: true

        });

        emit OracleUpdated(

            recordCounter,

            energyPrice,

            block.timestamp

        );

    }

    /* ---------------------------------------------------------------------- */
    /* Validation                                                             */
    /* ---------------------------------------------------------------------- */

    function validateEnergyRecord(

        uint256 energyAmount,

        uint256 totalCost

    )

        external

        returns (bool)

    {

        require(

            latestEnergyPrice > 0,

            "OracleManager: oracle unavailable"

        );

        require(

            block.timestamp <= lastUpdated + MAX_DATA_AGE,

            "OracleManager: oracle data expired"

        );

        bool status =

            (energyAmount * latestEnergyPrice) == totalCost;

        emit OracleValidation(

            energyAmount,

            totalCost,

            status

        );

        return status;

    }

    /* ---------------------------------------------------------------------- */
    /* View Functions                                                         */
    /* ---------------------------------------------------------------------- */

    function getLatestPrice()

        external

        view

        returns(uint256)

    {

        return latestEnergyPrice;

    }

    function getLastUpdate()

        external

        view

        returns(uint256)

    {

        return lastUpdated;

    }

    function totalOracleRecords()

        external

        view

        returns(uint256)

    {

        return recordCounter;

    }

}