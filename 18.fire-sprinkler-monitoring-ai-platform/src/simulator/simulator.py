import os,time,uuid,random,requests
from datetime import datetime,timezone
API=os.getenv("API_BASE_URL","http://localhost:8080"); delay=float(os.getenv("INTERVAL_SECONDS","3"))
POINTS={"WET-001":["NO_FLOW","FLOW"],"WET-002":["NORMAL","ABNORMAL"],"WET-003":["OPEN","CLOSED"],"WET-004":["STOPPED","RUNNING"],"WET-005":["NORMAL","FAULT"],"WET-006":["NORMAL","LOW"],"WET-007":["NORMAL","LOW_PRESSURE"],"DRY-001":["NORMAL","LOW_AIR"],"DRY-002":["NORMAL","HIGH_AIR"],"DRY-003":["NORMAL","OPERATED"],"DRY-004":["NO_FLOW","FLOW"],"DRY-005":["STOPPED","RUNNING"],"DRY-006":["NORMAL","FAULT"],"DRY-007":["NORMAL","LOW_PRESSURE"],"DRY-008":["OPEN","CLOSED"]}
s=requests.Session(); n=0
while True:
 p=random.choice(list(POINTS)); vals=POINTS[p]; n+=1; body={"eventId":str(uuid.uuid4()),"sourceId":"SIMULATOR-01","pointId":p,"previousValue":vals[0],"observedValue":vals[1],"quality":"GOOD","occurredAt":datetime.now(timezone.utc).isoformat(),"sequenceNumber":n}
 try: print(p,s.post(API+"/api/events",json=body,timeout=5).status_code,flush=True)
 except requests.RequestException as e: print("API not ready",e,flush=True)
 time.sleep(delay)
