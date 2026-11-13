# Fire Sprinkler Monitoring & AI Analytics Platform

Angular + ASP.NET Core 10 + Python FastAPI + PostgreSQL starter for read-only wet/dry sprinkler monitoring, event history and advisory analytics.

## Run locally
Requirements: Docker Desktop / Docker Compose.
```bash
docker compose up --build
```
- Angular: http://localhost:4200
- .NET Swagger: http://localhost:8080/swagger
- Python API: http://localhost:8001/docs
- PostgreSQL: localhost:5432

A synthetic simulator posts events for the 15 supplied wet/dry points. This is a development demonstration, not a certified or listed fire alarm system. It must not control, reset, suppress, delay or alter life-safety functions. Connect to live equipment only through a manufacturer-approved read-only interface after review by the fire protection engineer and relevant authority. The supplied point classifications are illustrative and must be checked against the approved cause-and-effect matrix.

## Components
- `src/api`: ASP.NET Core REST API, PostgreSQL persistence and SignalR event hub.
- `src/frontend`: Angular dashboard.
- `src/ml-service`: Python advisory state-transition analytics.
- `src/simulator`: synthetic event generator.
- `infra/terraform`: Azure resource-group starter; extend with networking, identity, Container Apps, PostgreSQL, Event Hubs and Key Vault.

## APIs
`GET /api/health`, `GET /api/points?systemType=WET`, `GET /api/events?limit=100`, `GET /api/summary`, `POST /api/events`, `GET /api/analytics/health`, `GET /api/analytics/pressure?pointId=DRY-001`, SignalR `/hubs/monitoring`.

POST event example:
```json
{"eventId":"evt-demo-1","sourceId":"SIMULATOR-01","pointId":"WET-001","observedValue":"FLOW","previousValue":"NO_FLOW","quality":"GOOD","occurredAt":"2026-11-14T12:00:00Z","sequenceNumber":1}
```

Classification is derived by the API from the configured point; clients cannot override it. The current summary reports event-record counts, not active/latching alarm state. ML output is advisory only and never changes event classification.

## Production hardening still required
Entra ID authentication and authorization, tenant/site isolation, TLS/private endpoints, managed identity, Key Vault, schema migrations, audit controls, monitoring, backup/restore, retention policies, threat modelling, load testing, vendor integration validation and fire-protection engineering approval. Terraform is a starter, not a complete production landing zone.
