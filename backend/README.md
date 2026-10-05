# Backend — MarketSim AI

Everything server-side lives here (monorepo under `backend/`).

```
backend/
├── api/          Spring Boot — public REST + WebSocket + auth
├── ai/           FastAPI — ML / XAI / NLP (called only by Spring)
└── contracts/    Solidity + Hardhat — Sepolia audit layer
```

| Folder | Role | Called by |
|--------|------|-----------|
| `api/` | Business CRUD, JWT, orchestration | Browser |
| `ai/` | Predictions, sentiment, agent, XAI | Spring only |
| `contracts/` | Hash anchoring + later insurance/badges | Spring (via web3) |

See each subfolder README and [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md).
