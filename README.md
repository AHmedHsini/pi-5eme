# MarketSim AI

Simulateur intelligent de salle de marché — Esprit PIF 2026-2027.

Plateforme de trading virtuel avec formation, analyse financière, agents IA, stress testing bancaire, actuariat et traçabilité blockchain (Sepolia).

## Stack

| Couche | Technologie |
|--------|-------------|
| Frontend | React + TypeScript (Vite) |
| API | Spring Boot 3 + JPA + Spring Security |
| Base de données | PostgreSQL 16 |
| IA / ML | FastAPI (Python) |
| Blockchain | Solidity + Hardhat (Ethereum Sepolia) |

## Modules

| # | Module | Rôle |
|---|--------|------|
| 1 | Utilisateurs & Administration | Comptes, rôles, back-office, sécurité |
| 2 | Trading & Gestion du Risque | Ordres, portefeuille, stop-loss / take-profit |
| 3 | Analyse Financière & Backtesting | Indicateurs, stratégies, backtests |
| 4 | Formation & Pédagogie | Cours, quiz, défis, progression |
| 5 | Marché, Prédiction & Sentiment | Cotations, prédictions, NLP |
| 6 | Agent de Trading Intelligent | Agent autonome + XAI |
| 7 | Stress Testing & Actuariat | Scénarios bancaires, primes, SHAP/LIME |

Chaque module combine une partie **CRUD** et une partie **IA**.

## Structure du dépôt

```
pi-5eme/
??? frontend/                 # React + Vite + TypeScript
??? backend/
?   ??? api/                  # Spring Boot (API publique)
?   ??? ai/                   # FastAPI (ML / XAI, interne)
?   ??? contracts/            # Smart contracts Sepolia
??? infra/                    # Docker Compose + variables d'env
??? docs/                     # Architecture détaillée
??? MarketSim_AI_Cahier_Projet.pdf
```

## Architecture (aperçu)

```
React  ?  Spring Boot  ?  PostgreSQL
               ?
               ??? FastAPI (inférence IA)
               ??? Sepolia (ancrage de hashes)
```

- Le navigateur appelle uniquement Spring Boot (`/api`, WebSocket).
- PostgreSQL est la source de vérité.
- La blockchain stocke des empreintes (hashes), pas les données métier complètes.

Détails : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Prérequis

- Node.js 20+
- Java 17+
- Python 3.12+
- Docker Desktop
- Git

## Démarrage rapide

### 1. Base de données

```bash
cp infra/.env.example infra/.env
docker compose -f infra/docker-compose.yml up postgres
```

### 2. Service IA

```bash
cd backend/ai
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. API Spring

Générer le projet Spring Boot dans `backend/api/` (voir `backend/api/README.md`), puis :

```bash
cd backend/api
./mvnw spring-boot:run
```

### 4. Frontend

Scaffold Vite dans `frontend/` (voir `frontend/README.md`), puis :

```bash
cd frontend
npm install
npm run dev
```

### URLs locales

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| API Spring | http://localhost:8080 |
| Docs FastAPI | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

## Documentation

| Fichier | Contenu |
|---------|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture, modules, phases, conventions |
| [backend/README.md](backend/README.md) | Vue d'ensemble backend |
| [frontend/README.md](frontend/README.md) | Setup frontend |
| [MarketSim_AI_Cahier_Projet.pdf](MarketSim_AI_Cahier_Projet.pdf) | Cahier de projet |

## Équipe

Équipe PIF — Esprit · Année universitaire 2026-2027
