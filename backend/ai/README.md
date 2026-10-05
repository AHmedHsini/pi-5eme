# Backend AI — FastAPI

Internal ML / XAI / NLP worker. **Spring Boot (`backend/api`) is the only public API.**

Path in monorepo: `backend/ai/`

## Run locally

```bash
cd backend/ai
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs

## Implemented stubs

| Route | Purpose |
|-------|---------|
| `GET /health` | Liveness |
| `POST /predict/risk` | Position risk placeholder |
| `POST /sentiment/news` | News sentiment placeholder |
| `POST /xai/explain` | XAI placeholder |

Add real models under `app/models/` and keep request/response schemas stable for Spring.
