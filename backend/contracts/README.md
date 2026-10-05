# Backend contracts — Sepolia

MVP: `AuditRegistry` anchors content hashes from Spring after DB writes.

Path in monorepo: `backend/contracts/`

## Setup

```bash
cd backend/contracts
npm init -y
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox dotenv
npx hardhat init   # TypeScript or JS
```

`AuditRegistry.sol` is already under `contracts/contracts/`.

## Deploy to Sepolia

1. Get a Sepolia RPC (Alchemy/Infura) and a funded test wallet.
2. Set `SEPOLIA_RPC_URL` and `SEPOLIA_PRIVATE_KEY` in `infra/.env`.
3. Deploy and copy the address into `AUDIT_REGISTRY_ADDRESS` for Spring.

## What to anchor (MVP)

| refType | When |
|---------|------|
| `TRADE` | Order filled |
| `BACKTEST` | Backtest finished |
| `STRESS` | Stress scenario result |
| `XAI` | Explanation generated |
| `AGENT` | Agent decision recorded |

Phase 2: parametric insurance SC + learning badges/NFTs.
