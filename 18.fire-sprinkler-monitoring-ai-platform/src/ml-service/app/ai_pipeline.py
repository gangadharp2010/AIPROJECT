import json, os
from datetime import datetime, timezone
from typing import Any
import numpy as np
import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.ensemble import IsolationForest
from openai import AzureOpenAI

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://appuser:admin%40123@postgres:5432/firesprinkler")
# Fictional demo baselines only. Not engineering limits, setpoints or alarm thresholds.
BASELINES = {
 "WET-002": (100.0, 4.0, "psi", "Wet water pressure"),
 "WET-006": (75.0, 5.0, "%", "Water tank level"),
 "WET-007": (95.0, 4.0, "psi", "Water supply pressure"),
 "DRY-001": (42.0, 2.0, "psi", "Dry air pressure"),
 "DRY-002": (48.0, 2.0, "psi", "Dry air pressure monitor"),
 "DRY-007": (90.0, 4.0, "psi", "Dry water supply pressure"),
}
MODELS = {}

def db():
    return psycopg.connect(DATABASE_URL)

def ensure_schema():
    sql = (
      'CREATE TABLE IF NOT EXISTS "TelemetryReadings" ('
      '"Id" BIGSERIAL PRIMARY KEY,"PointId" VARCHAR(50) NOT NULL,'
      '"NumericValue" DOUBLE PRECISION NOT NULL,"Unit" VARCHAR(20) NOT NULL,'
      '"Quality" VARCHAR(30) NOT NULL DEFAULT \'GOOD\',"OccurredAt" TIMESTAMPTZ NOT NULL,'
      '"ReceivedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW(),"SourceId" VARCHAR(100));'
      'CREATE INDEX IF NOT EXISTS "IX_TelemetryReadings_Point_Time" ON "TelemetryReadings" ("PointId","OccurredAt" DESC);'
      'CREATE TABLE IF NOT EXISTS "MlPredictions" ('
      '"Id" BIGSERIAL PRIMARY KEY,"PointId" VARCHAR(50) NOT NULL,'
      '"TelemetryReadingId" BIGINT REFERENCES "TelemetryReadings"("Id"),'
      '"ModelName" VARCHAR(100) NOT NULL,"ModelVersion" VARCHAR(50) NOT NULL,'
      '"AnomalyScore" DOUBLE PRECISION NOT NULL,"IsAnomaly" BOOLEAN NOT NULL,'
      '"Explanation" TEXT NOT NULL,"AdvisoryOnly" BOOLEAN NOT NULL DEFAULT TRUE,'
      '"CreatedAt" TIMESTAMPTZ NOT NULL DEFAULT NOW());'
      'CREATE INDEX IF NOT EXISTS "IX_MlPredictions_Point_Created" ON "MlPredictions" ("PointId","CreatedAt" DESC);'
    )
    with db() as c:
        c.execute(sql)
        c.commit()

def model_for(point_id):
    if point_id not in BASELINES:
        raise HTTPException(400, f"No numeric demo baseline configured for {point_id}")
    if point_id not in MODELS:
        mean, std, _, _ = BASELINES[point_id]
        rng = np.random.default_rng(100 + sum(map(ord, point_id)))
        train = rng.normal(mean, std, (1500, 1))
        MODELS[point_id] = IsolationForest(n_estimators=150, contamination=0.03, random_state=42).fit(train)
    return MODELS[point_id]

class TelemetryIn(BaseModel):
    pointId: str
    numericValue: float
    unit: str
    quality: str = "GOOD"
    occurredAt: datetime | None = None
    sourceId: str = "SIMULATOR"

class ChatIn(BaseModel):
    question: str = Field(min_length=3, max_length=1000)

app = FastAPI(title="Fire Sprinkler ML & GenAI Advisory API", version="0.1.0")

@app.on_event("startup")
def startup():
    ensure_schema()

@app.get("/health")
def health():
    try:
        with db() as c: c.execute("SELECT 1")
        return {"status":"healthy","database":"connected","mode":"advisory"}
    except Exception as e:
        raise HTTPException(503, str(e))

@app.get("/points")
def points():
    return {"points":[{"pointId":k,"mean":v[0],"std":v[1],"unit":v[2],"label":v[3],
                       "baselineType":"synthetic-demo-only"} for k,v in BASELINES.items()]}

@app.post("/telemetry")
def ingest(x: TelemetryIn):
    if x.pointId not in BASELINES:
        raise HTTPException(400, f"Unsupported numeric demo point: {x.pointId}")
    if x.quality.upper() != "GOOD":
        raise HTTPException(422, "Only GOOD-quality readings are scored.")
    mean,std,unit,label = BASELINES[x.pointId]
    if x.unit != unit:
        raise HTTPException(422, f"Expected demo unit {unit} for {x.pointId}")
    model = model_for(x.pointId)
    raw = float(model.score_samples(np.array([[x.numericValue]]))[0])
    rng = np.random.default_rng(7)
    threshold = float(np.quantile(model.score_samples(rng.normal(mean,std,(1000,1))),0.03))
    flagged = raw < threshold
    score = float(np.clip((threshold-raw)/max(abs(threshold),1e-6),0,1))
    explanation = (f"{x.numericValue:.2f} {unit} is unusual relative to the synthetic demo baseline for {label}."
                   if flagged else f"{x.numericValue:.2f} {unit} is within the synthetic demo model's expected pattern.")
    occurred = x.occurredAt or datetime.now(timezone.utc)
    with db() as c:
        rid = c.execute('INSERT INTO "TelemetryReadings" ("PointId","NumericValue","Unit","Quality","OccurredAt","SourceId") VALUES (%s,%s,%s,%s,%s,%s) RETURNING "Id"',
          (x.pointId,x.numericValue,x.unit,x.quality.upper(),occurred,x.sourceId)).fetchone()[0]
        pid = c.execute('INSERT INTO "MlPredictions" ("PointId","TelemetryReadingId","ModelName","ModelVersion","AnomalyScore","IsAnomaly","Explanation","AdvisoryOnly") VALUES (%s,%s,\'IsolationForest\',\'demo-0.1\',%s,%s,%s,TRUE) RETURNING "Id"',
          (x.pointId,rid,score,flagged,explanation)).fetchone()[0]
        c.commit()
    return {"readingId":rid,"predictionId":pid,"pointId":x.pointId,"anomalyDetected":flagged,
            "anomalyScore":round(score,4),"model":"IsolationForest","modelVersion":"demo-0.1",
            "explanation":explanation,"advisoryOnly":True,"baselineType":"synthetic-demo-only"}

@app.get("/anomalies")
def anomalies(limit:int=50):
    limit=max(1,min(limit,200))
    with db() as c:
        rows=c.execute('SELECT p."Id",p."PointId",t."NumericValue",t."Unit",p."AnomalyScore",p."Explanation",p."CreatedAt" FROM "MlPredictions" p JOIN "TelemetryReadings" t ON t."Id"=p."TelemetryReadingId" WHERE p."IsAnomaly"=TRUE ORDER BY p."CreatedAt" DESC LIMIT %s',(limit,)).fetchall()
    return {"items":[{"predictionId":r[0],"pointId":r[1],"value":r[2],"unit":r[3],"anomalyScore":r[4],
      "explanation":r[5],"createdAt":r[6].isoformat(),"advisoryOnly":True} for r in rows]}

def evidence(question):
    q=question.lower()
    with db() as c:
        a=c.execute('SELECT p."PointId",t."NumericValue",t."Unit",p."AnomalyScore",p."Explanation",p."CreatedAt" FROM "MlPredictions" p JOIN "TelemetryReadings" t ON t."Id"=p."TelemetryReadingId" WHERE p."IsAnomaly"=TRUE ORDER BY p."CreatedAt" DESC LIMIT 10').fetchall()
        t=c.execute('SELECT "PointId","NumericValue","Unit","Quality","OccurredAt" FROM "TelemetryReadings" ORDER BY "OccurredAt" DESC LIMIT 15').fetchall()
        e=[]
        if any(w in q for w in ("event","alarm","supervisory","trouble","today","recent")):
            e=c.execute('SELECT "PointId","Classification","ObservedValue","OccurredAt" FROM "Events" ORDER BY "OccurredAt" DESC LIMIT 20').fetchall()
    return {"question":question,
      "anomalies":[{"pointId":r[0],"value":r[1],"unit":r[2],"score":r[3],"explanation":r[4],"createdAt":r[5].isoformat()} for r in a],
      "telemetry":[{"pointId":r[0],"value":r[1],"unit":r[2],"quality":r[3],"occurredAt":r[4].isoformat()} for r in t],
      "events":[{"pointId":r[0],"classification":r[1],"observedValue":r[2],"occurredAt":r[3].isoformat()} for r in e]}

@app.post("/ai/chat")
def chat(x:ChatIn):
    data=evidence(x.question)
    endpoint,key,deployment=(os.getenv(k) for k in ("AZURE_OPENAI_ENDPOINT","AZURE_OPENAI_API_KEY","AZURE_OPENAI_DEPLOYMENT"))
    if endpoint and key and deployment:
        try:
            client=AzureOpenAI(azure_endpoint=endpoint,api_key=key,api_version=os.getenv("AZURE_OPENAI_API_VERSION","2024-10-21"))
            out=client.chat.completions.create(model=deployment,temperature=0.1,messages=[
              {"role":"system","content":"Read-only fire sprinkler reporting assistant. Use only supplied JSON evidence. If missing say Cannot be confirmed from available information. Distinguish panel events from ML advisory anomalies. Never claim safety, diagnose confirmed failure, change setpoints, or advise resetting/suppressing alarms. Mention synthetic demo baselines."},
              {"role":"user","content":json.dumps(data,default=str)}])
            answer=out.choices[0].message.content or "Cannot be confirmed from available information."
            provider="azure-openai"
        except Exception:
            answer="Azure OpenAI is configured but unavailable. Review the returned evidence snapshot."
            provider="fallback"
    else:
        n=len(data["anomalies"])
        answer=(f"The evidence snapshot contains {n} stored advisory anomaly record(s). These are model observations based on synthetic demo baselines, not fire alarms or confirmed equipment failures. Check the recorded evidence and authoritative fire panel."
                if n else "No stored ML anomaly records were found in this evidence snapshot. This does not establish that the system is normal or safe. Use the authoritative fire panel and approved site procedures.")
        provider="evidence-template"
    return {"answer":answer,"provider":provider,"evidence":data,"advisoryOnly":True}
