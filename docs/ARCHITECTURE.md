# MarketSim AI — Architecture

**Stack:** React + TypeScript · Spring Boot 3 + JPA · PostgreSQL · FastAPI · Ethereum Sepolia  
**Repo:** **Monorepo** with `frontend/` + `backend/` at the root  
**Project:** Simulateur intelligent de salle de marche (Esprit PIF 2026-2027)

---

## 1. Goals

- Support 7 autonomous modules (CRUD + AI each).
- Keep PostgreSQL as the **source of truth**.
- Treat blockchain as a **trust / audit layer** (hashes + limited smart contracts).
- Isolate ML in Python so Spring stays focused on API, auth, and orchestration.

---

## 2. High-level system

```
  React SPA  --REST+JWT / WebSocket-->  Spring Boot (public API)
                                            |
                 +--------------------------+--------------------------+
                 |                          |                          |
                 v                          v                          v
            PostgreSQL                   FastAPI                     Sepolia
            (JPA / CRUD)                (ML / XAI)                  (hashes)
```

**Rule:** the browser never calls FastAPI or the chain directly. Spring is the only public API.

---

## 3. Services

| Service | Path | Tech | Port | Responsibility |
|---------|------|------|------|----------------|
| `web` | `frontend/` | React + Vite + TS | 5173 | UI, charts, WS client |
| `api` | `backend/api/` | Spring Boot 3 + JPA | 8080 | Auth, CRUD, trading, orchestration |
| `ai` | `backend/ai/` | FastAPI | 8000 | Inference, XAI, NLP, agent |
| `db` | Docker | PostgreSQL 16 | 5432 | Persistent data |
| `contracts` | `backend/contracts/` | Hardhat + Solidity | — | Deploy/read Sepolia |

Optional later: Redis (cache / rate-limit), MinIO (course files).

---

## 4. Module mapping

| # | Module | Spring package | FastAPI routes | Chain use |
|---|--------|----------------|----------------|-----------|
| 1 | Users & Admin | `users` | anomaly score, user-level score | audit of sensitive admin actions (hash) |
| 2 | Trading & Risk | `trading` | position risk, SL/TP suggestion | immutable trade hash |
| 3 | Analysis & Backtesting | `analysis` | trend in backtest, strategy compare | backtest result hash |
| 4 | Learning | `learning` | content recommend, quiz generation | NFT / certificate attestations |
| 5 | Market & Sentiment | `market` | LSTM/Prophet, news sentiment | prediction reliability anchor (optional) |
| 6 | Trading Agent | `agent` | RL/rules decide + XAI text | agent decision + explanation hash |
| 7 | Stress & Actuarial | `stress` | stress impact, premiums, SHAP/LIME | scenario + XAI hash; parametric insurance SC |

Shared packages in Spring: `security`, `common`, `ai` (HTTP client), `blockchain`.

---

## 5. Communication patterns

### 5.1 Client ? Spring

- `POST /api/auth/register|login`
- `GET/POST/PUT/DELETE /api/{module}/...` (JWT Bearer)
- WebSocket `/ws` ? topics `/topic/quotes`, `/topic/orders/{userId}`

### 5.2 Spring ? FastAPI (internal)

- Docker network only; not exposed to the browser.
- Sync HTTP for interactive UX; async jobs later if models are slow.
- Spring persists every AI result.

### 5.3 Spring ? Sepolia

- After durable DB write, compute `sha256(payload)`.
- Call `AuditRegistry.anchor(bytes32 hash, string refType, string refId)`.
- Store `txHash` + `blockNumber` on the Postgres row (`blockchain_anchors`).

---

## 6. Auth & security

- Spring Security + JWT.
- Roles: `USER`, `ADMIN` (+ optional `INSTRUCTOR`).
- Password hashing: BCrypt.
- CORS locked to frontend origin.
- FastAPI not public in production.
- Secrets via env / `.env` (never commit).

---

## 7. Data model (logical)

Core entities (owned by Spring/JPA):

- `User`, `Role`, `ActivityLog`
- `Asset`, `Quote`, `NewsItem`
- `Portfolio`, `Position`, `Order`, `Transaction`
- `RiskLimit` (stop-loss / take-profit / exposure)
- `Strategy`, `IndicatorConfig`, `BacktestRun`
- `Course`, `Quiz`, `Challenge`, `Progress`, `Badge`
- `Prediction`, `SentimentScore`
- `TradingAgent`, `AgentDecision`
- `BankProfile`, `StressScenario`, `StressResult`
- `InsuranceContract`, `Claim`
- `BlockchainAnchor` (entityType, entityId, contentHash, txHash, network)

FastAPI may read features via API or a read-only DB role; it does **not** own schema migrations.

---

## 8. Real-time market path

1. Market ingest (mock generator or external API) in Spring.
2. Quotes saved to `Quote`.
3. Spring broadcasts to `/topic/quotes`.
4. Trading engine simulates fills against latest price.
5. UI updates via WS + REST.

MVP: **mock price feed**. Swap later for a public market API.

---

## 9. AI architecture

| Capability | Suggested library | Notes |
|------------|-------------------|-------|
| Trend | Prophet and/or LSTM (PyTorch) | Start with Prophet for MVP |
| Sentiment | transformers or lighter model | News batch job |
| Risk / SL-TP | classical ML or volatility rules | Fast, explainable |
| Agent | rules first, then RL | Pedagogy > profitability |
| XAI | SHAP / LIME | Human-readable summary |
| Actuarial | closed-form + simple GLM | Premiums, claim probability |

Persist every inference with: model version, inputs hash, output, latency, optional explanation id.

---

## 10. Blockchain scope (MVP ? later)

**MVP**

1. `AuditRegistry` on Sepolia — `anchor(hash, refType, refId)`.
2. Anchor trades, backtests, stress results, XAI explanations.

**Phase 2**

3. Parametric insurance smart contract (Module 7 demo).
4. Simple NFT / badge attestations for learning.

Do **not** put order books or user PII on-chain.

---

## 11. Repository layout (monorepo)

**Yes — use one Git monorepo.** Top level is `frontend/` and `backend/`.

```
marketsim/                      ? single Git repository
??? frontend/                   # React + Vite + TypeScript
?   ??? src/
?       ??? app/
?       ??? features/           # one folder per module
?       ??? shared/             # ui, api client, ws, auth
??? backend/
?   ??? api/                    # Spring Boot (public API)
?   ??? ai/                     # FastAPI (ML / XAI)
?   ??? contracts/              # Hardhat + Solidity
??? infra/
?   ??? docker-compose.yml
?   ??? .env.example
??? docs/
?   ??? ARCHITECTURE.md
??? README.md
```

### Why monorepo

- Frontend and API ship together in the same PR
- One Docker Compose, one env, one architecture doc
- Still clear ownership: `frontend/` vs `backend/api` vs `backend/ai`
- Best fit for a student team / jury demo

Split into multiple Git repos only if a teacher requires it.

### Spring packages (`backend/api`)

```
com.marketsim
  ??? MarketSimApplication
  ??? config
  ??? security
  ??? users | trading | analysis | learning | market | agent | stress
  ??? ai            # WebClient ? FastAPI
  ??? blockchain    # Sepolia
  ??? common
```

---

## 12. Local runtime

```bash
docker compose -f infra/docker-compose.yml up postgres
# later, full stack:
docker compose -f infra/docker-compose.yml --profile full up --build
```

- Web: http://localhost:5173
- API: http://localhost:8080/api
- AI docs: http://localhost:8000/docs
- DB: localhost:5432 / `marketsim`

---

## 13. Delivery phases

| Phase | Focus | Exit criteria |
|-------|--------|----------------|
| P0 | Monorepo, auth, users, docker | Login + role-protected hello |
| P1 | Trading CRUD + mock quotes + WS | Place order, see portfolio update |
| P2 | Market + one FastAPI model | Prediction stored + shown |
| P3 | Analysis backtest + learning CRUD | Strategy save + quiz |
| P4 | Agent + XAI + stress/actuarial | Explained decision + stress run |
| P5 | Sepolia anchors + demo contracts | On-chain hash for trades/results |
| P6 | Hardening, admin, demos | Jury-ready |

---

## 14. Team ownership (example)

| Person | Owns |
|--------|------|
| A | `backend/api` users/security + `frontend` shell/auth |
| B | Trading + market feed + WS |
| C | `backend/ai` models + Spring `ai` client |
| D | Learning + analysis UI/API |
| E | Stress/actuarial + `backend/contracts` |

---

## 15. Non-goals

- Real money / real brokerage
- Mainnet deployment
- Hyperledger Fabric (unless required)
- Replacing Postgres with on-chain storage
- Training huge models on every request

---

## 16. Decision log

| Decision | Choice | Why |
|----------|--------|-----|
| Repo | Monorepo (`frontend/` + `backend/`) | One team, one demo, shared infra |
| Public API | Spring only | One auth boundary |
| ORM | JPA/Hibernate | Native to Spring |
| AI runtime | FastAPI under `backend/ai` | Python ML ecosystem |
| Chain | Sepolia + Solidity | Cheap audit demo |
| DB | PostgreSQL | Relational fit for trading + admin |
| Frontend | React + TS in `frontend/` | Dashboards + real-time UI |
