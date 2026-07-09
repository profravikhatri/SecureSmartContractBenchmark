// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

/**
 * -----------------------------------------------------------------------------
 * SecureSmartContractBenchmark
 * -----------------------------------------------------------------------------
 * Contract : AccessManager
 *
 * Description:
 * Provides lightweight role-based authorization for blockchain
 * benchmark experiments.
 *
 * Responsibilities:
 * - Contract ownership
 * - Authorized participant management
 * - Role validation
 * - Access event logging
 *
 * -----------------------------------------------------------------------------
 */

contract AccessManager {

    /// @notice Contract administrator
    address public owner;

    /// @notice Authorized blockchain participants
    mapping(address => bool) private authorizedUsers;

    /// @notice Total authorized users
    uint256 public authorizedUserCount;

    /* -------------------------------------------------------------------------- */
    /*                                   Events                                   */
    /* -------------------------------------------------------------------------- */

    event UserAuthorized(
        address indexed account,
        address indexed grantedBy,
        uint256 timestamp
    );

    event UserRevoked(
        address indexed account,
        address indexed revokedBy,
        uint256 timestamp
    );

    event OwnershipTransferred(
        address indexed previousOwner,
        address indexed newOwner
    );

    /* -------------------------------------------------------------------------- */
    /*                                  Modifiers                                 */
    /* -------------------------------------------------------------------------- */

    modifier onlyOwner() {
        require(msg.sender == owner, "AccessManager: owner only");
        _;
    }

    modifier onlyAuthorized() {
        require(
            authorizedUsers[msg.sender],
            "AccessManager: unauthorized user"
        );
        _;
    }

    /* -------------------------------------------------------------------------- */
    /*                                Constructor                                 */
    /* -------------------------------------------------------------------------- */

    constructor() {
        owner = msg.sender;

        authorizedUsers[msg.sender] = true;

        authorizedUserCount = 1;

        emit UserAuthorized(
            msg.sender,
            msg.sender,
            block.timestamp
        );
    }

    /* -------------------------------------------------------------------------- */
    /*                           Authorization Functions                          */
    /* -------------------------------------------------------------------------- */

    /**
     * @notice Authorize a participant
     * @param account Blockchain account
     */
    function authorizeUser(
        address account
    )
        external
        onlyOwner
    {
        require(
            account != address(0),
            "AccessManager: invalid address"
        );

        require(
            !authorizedUsers[account],
            "AccessManager: already authorized"
        );

        authorizedUsers[account] = true;

        unchecked {
            authorizedUserCount++;
        }

        emit UserAuthorized(
            account,
            msg.sender,
            block.timestamp
        );
    }

    /**
     * @notice Revoke participant authorization
     * @param account Blockchain account
     */
    function revokeUser(
        address account
    )
        external
        onlyOwner
    {
        require(
            authorizedUsers[account],
            "AccessManager: user not authorized"
        );

        require(
            account != owner,
            "AccessManager: cannot revoke owner"
        );

        authorizedUsers[account] = false;

        unchecked {
            authorizedUserCount--;
        }

        emit UserRevoked(
            account,
            msg.sender,
            block.timestamp
        );
    }

    /* -------------------------------------------------------------------------- */
    /*                             View Functions                                 */
    /* -------------------------------------------------------------------------- */

    /**
     * @notice Check authorization status
     */
    function isAuthorized(
        address account
    )
        public
        view
        returns (bool)
    {
        return authorizedUsers[account];
    }

    /**
     * @notice Returns repository administrator
     */
    function getOwner()
        external
        view
        returns (address)
    {
        return owner;
    }

    /* -------------------------------------------------------------------------- */
    /*                           Ownership Management                             */
    /* -------------------------------------------------------------------------- */

    /**
     * @notice Transfer contract ownership
     */
    function transferOwnership(
        address newOwner
    )
        external
        onlyOwner
    {
        require(
            newOwner != address(0),
            "AccessManager: invalid owner"
        );

        authorizedUsers[newOwner] = true;

        emit OwnershipTransferred(
            owner,
            newOwner
        );

        owner = newOwner;
    }
}