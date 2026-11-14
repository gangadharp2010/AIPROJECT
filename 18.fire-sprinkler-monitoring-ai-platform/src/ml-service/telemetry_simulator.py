import os, random, time, requests
from datetime import datetime, timezone
BASE=os.getenv("ML_BASE_URL","http://ml-service:8001")
DELAY=float(os.getenv("TELEMETRY_INTERVAL_SECONDS","5"))
# Fictional demo data only; not alarm thresholds, design values or operating limits.
POINTS={"WET-002":(100,4,"psi"),"WET-006":(75,5,"%"),"WET-007":(95,4,"psi"),
        "DRY-001":(42,2,"psi"),"DRY-002":(48,2,"psi"),"DRY-007":(90,4,"psi")}
s=requests.Session()
while True:
    p=random.choice(list(POINTS)); mean,std,unit=POINTS[p]
    value=random.gauss(mean,std)
    if random.random()<0.035: value+=random.choice([-1,1])*std*random.uniform(4,7)
    body={"pointId":p,"numericValue":round(value,3),"unit":unit,"quality":"GOOD",
          "occurredAt":datetime.now(timezone.utc).isoformat(),"sourceId":"DEMO-TELEMETRY-SIMULATOR"}
    try:
        r=s.post(f"{BASE}/telemetry",json=body,timeout=5); print(r.status_code,r.text[:250],flush=True)
    except Exception as e: print("send failed:",e,flush=True)
    time.sleep(DELAY)
