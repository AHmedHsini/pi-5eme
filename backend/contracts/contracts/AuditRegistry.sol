// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title AuditRegistry — anchors content hashes for MarketSim AI
/// @notice Stores sha256 hashes of trades, backtests, stress results, XAI explanations.
///         Full payloads stay in PostgreSQL; only hashes live on-chain.
contract AuditRegistry {
    event Anchored(
        bytes32 indexed contentHash,
        string refType,
        string refId,
        address indexed sender,
        uint256 timestamp
    );

    mapping(bytes32 => bool) public anchored;

    function anchor(
        bytes32 contentHash,
        string calldata refType,
        string calldata refId
    ) external {
        require(contentHash != bytes32(0), "empty hash");
        require(!anchored[contentHash], "already anchored");
        anchored[contentHash] = true;
        emit Anchored(contentHash, refType, refId, msg.sender, block.timestamp);
    }
}
