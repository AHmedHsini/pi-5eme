# MarketSim AI

Intelligent market-floor simulator — Esprit PIF 2026-2027.

**Stack:** React + TypeScript · Spring Boot 3 + JPA · PostgreSQL · FastAPI · Sepolia  
**Repo style:** **Monorepo** — one Git repo, `frontend/` + `backend/` at the root.

## Layout

```
marketsim/                 ? single Git repository (monorepo)
??? frontend/              React + Vite + TypeScript
??? backend/
?   ??? api/               Spring Boot (public API)
?   ??? ai/                FastAPI (ML / XAI, internal)
?   ??? contracts/         Hardhat + Solidity (Sepolia)
??? infra/                 Docker Compose + env
??? docs/                  Architecture
??? README.md
```

## Can we use a monorepo?

**Yes — and you should.** One repo for frontend + backend is ideal here:

- One PR can touch UI + API together
- Shared docs, Docker, and env in one place
- Easier for the team and for the jury demo
- Still clear ownership: `frontend/` vs `backend/api` vs `backend/ai`

You do **not** need separate repos unless teachers force it.

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Quick start

```bash
cp infra/.env.example infra/.env
docker compose -f infra/docker-compose.yml up postgres
```

| Piece | Path | URL (local) |
|-------|------|-------------|
| Frontend | `frontend/` | http://localhost:5173 |
| Spring API | `backend/api/` | http://localhost:8080 |
| FastAPI | `backend/ai/` | http://localhost:8000/docs |
| Postgres | Docker | localhost:5432 |

## Design rules

1. Browser ? **Spring only** (`backend/api`).
2. **PostgreSQL** = source of truth.
3. Sepolia = **hashes**, not full rows.
4. FastAPI stays **internal** (called by Spring).
