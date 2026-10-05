# Backend API — Spring Boot

Public backend: auth, CRUD modules, WebSockets, FastAPI client, Sepolia anchoring.

Path in monorepo: `backend/api/`

## Create the project (once)

Use [Spring Initializr](https://start.spring.io) (or IDE) into this folder:

- Java 17+, Spring Boot 3.4.x
- Dependencies: Web, Security, Data JPA, Validation, WebSocket, Actuator, PostgreSQL driver
- Group: `com.marketsim` · Artifact: `api`

## Target package layout

```
com.marketsim
  ??? MarketSimApplication
  ??? config
  ??? security          # JWT filter, roles
  ??? users             # Module 1
  ??? trading           # Module 2
  ??? analysis          # Module 3
  ??? learning          # Module 4
  ??? market            # Module 5
  ??? agent             # Module 6
  ??? stress            # Module 7
  ??? ai                # WebClient ? backend/ai (FastAPI)
  ??? blockchain        # web3j / Sepolia
  ??? common            # errors, DTOs, pagination
```

## Local run (after scaffold)

```bash
docker compose -f ../../infra/docker-compose.yml up postgres
./mvnw spring-boot:run
```

Env (see `infra/.env.example`):

- `SPRING_DATASOURCE_*`
- `JWT_SECRET`
- `AI_BASE_URL=http://localhost:8000`

## API conventions

- Base path: `/api`
- Auth: `Authorization: Bearer <jwt>`
- WS: `/ws` + STOMP topics `/topic/quotes`, `/topic/orders/{userId}`
