from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
app=FastAPI(title="Fire Sprinkler Advisory Analytics",version="1.0.0")
class Observation(BaseModel): timestamp:Optional[datetime]=None; value:str
class Request(BaseModel): pointId:str; observations:list[Observation]
@app.get("/health")
def health(): return {"status":"healthy","mode":"advisory-only"}
@app.post("/analyze/states")
def analyze(req:Request):
 vals=[x.value for x in req.observations]; 
 counts={v:vals.count(v) for v in set(vals)}; 
 transitions=sum(vals[i]!=vals[i-1] for i in range(1,len(vals))); 
 rate=transitions/max(len(vals)-1,1)
 insight="Insufficient observations" if not vals else ("Frequent state changes observed; review event history and field conditions." if rate>0.5 and len(vals)>=5 else "No unusual transition frequency detected in this sample.")
 return {"pointId":req.pointId,"observationCount":len(vals),"stateCounts":counts,"transitionCount":transitions,"transitionRate":round(rate,3),"insight":insight,"advisory":True,"warning":"Not an alarm classification, diagnosis or instruction to alter a fire protection system."}
