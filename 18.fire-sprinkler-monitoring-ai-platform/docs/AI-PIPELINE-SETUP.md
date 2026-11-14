# Fire Sprinkler ML + GenAI overlay

## Apply
1. Back up the existing `src/ml-service` folder.
2. Merge this package's `src/ml-service` into your project.
3. Copy `docker-compose.ai.override.yml` to the project root.
4. Run from the project root:

```powershell
docker compose -f docker-compose.yml -f docker-compose.ai.override.yml up --build -d
```

Swagger: http://localhost:8001/docs

Verify:
```powershell
Invoke-RestMethod http://localhost:8001/health
Invoke-RestMethod http://localhost:8001/points
Invoke-RestMethod http://localhost:8001/anomalies
```

GenAI/evidence test:
```powershell
$body = @{ question = "Summarize recent dry sprinkler telemetry and anomalies" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8001/ai/chat" -Method Post -ContentType "application/json" -Body $body
```

Database tables: `TelemetryReadings`, `MlPredictions`.

## What is implemented
- Numeric telemetry ingestion and persistence.
- Per-point Isolation Forest anomaly scoring.
- Prediction history endpoint.
- Telemetry simulator.
- Evidence-bounded GenAI endpoint with optional Azure OpenAI. Without credentials it returns a deterministic evidence summary.

## Critical limitations
- All numeric values and model baselines are synthetic demo values, not engineering thresholds, setpoints or commissioning data.
- Isolation Forest is fitted to synthetic normal distributions at service startup. Its score is not a failure probability and this is not a validated field model.
- Only send numeric data when an approved sensor/interface actually provides it. Binary switches do not provide continuous PSI/level measurements.
- ML/GenAI are advisory only; never delay, suppress, reset, acknowledge, reclassify or control certified fire-panel signals.
- The event evidence query assumes the starter schema uses `"Events"` and quoted PascalCase columns. Adjust `evidence()` if your database differs.
- Before production add authentication, authorization, tenant scoping, rate limiting, audit, retention, prompt-injection controls, model evaluation, drift monitoring and approved RAG documents.
- Predictive failure models require labelled maintenance/failure outcomes, not merely alarm events.
