# Frontend — MarketSim AI

React + Vite + TypeScript SPA. Talks **only** to Spring (`backend/api`).

## Scaffold (once)

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
npm install react-router-dom @tanstack/react-query
```

If the folder is not empty, scaffold in a temp folder and move files in, or init Vite carefully.

Suggested structure after scaffold:

```
frontend/
  src/
    app/              # router, providers, layout
    features/
      auth/
      trading/
      analysis/
      learning/
      market/
      agent/
      stress/
      admin/
    shared/
      api/            # fetch client + JWT
      ws/             # WebSocket/STOMP
      ui/
  Dockerfile
  package.json
```

## Env

```
VITE_API_URL=http://localhost:8080/api
VITE_WS_URL=http://localhost:8080/ws
```

## Run

```bash
npm run dev
```
