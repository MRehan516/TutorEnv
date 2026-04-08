from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from environment import TutorEnvironment
from models import TeachingAction, ResetResult, StepResult
from tasks import TASK_REGISTRY

app = FastAPI(title="TutorEnv API", description="OpenEnv-compliant API for TutorEnv")
env = TutorEnvironment()

class ResetRequest(BaseModel):
    task_id: str = "easy_vaccine_misconception"

@app.get("/")
def read_root():
    return {"status": "TutorEnv is running", "valid_tasks": list(TASK_REGISTRY.keys())}

@app.post("/reset", response_model=ResetResult)
def reset(req: ResetRequest):
    try:
        result = env.reset(req.task_id)
        result.session_id = str(uuid.uuid4())
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/step", response_model=StepResult)
def step(action: TeachingAction):
    try:
        return env.step(action)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state", response_model=StepResult)
def get_state():
    try:
        return env.state()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
    
if __name__ == "__main__":
    main()