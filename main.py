from fastapi import FastAPI, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.AuthManager import AuthManager
from app.Orchestrator import Orchestrator
from app.ConfigLoader import ConfigLoader
from app.WorkflowManager import WorkflowManager
from app.Caller import Caller
from app.handlers.ErrorHandler import ErrorHandler

from typing import List

from app.models.RequestModel import RequestModel

app = FastAPI(
    title="ETL Orchestrator",
    openapi_prefix="/api",
)

config_loader = ConfigLoader()
caller = Caller()
authManager = AuthManager()
workflow_manager = WorkflowManager(config_loader.load_config('config/config.yaml'))
error_handler = ErrorHandler()
orchestrator = Orchestrator(workflow_manager, caller, config_loader)

@app.post("/v1/login")
def login( credentials: dict = Body(...)):
    try:
        return authManager.login(credentials)
    except Exception as e:
        error_handler.log_error(e)
        raise HTTPException(status_code=500, detail=e)

@app.post("/v1/start-process")
def start_process(data: RequestModel):
    try:
        response = orchestrator.start_process(data)

        if all(item["status"] == "success" for item in response):
            return {"status": "success", "message": "All processes completed successfully"}
        else:
            failed_processes = [item for item in response if item["status"] != "success"]
            error_message = f"Failed processes: {', '.join([item['process'] for item in failed_processes])}"
            raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        error_handler.log_error(str(e))
        raise HTTPException(status_code=500, detail=str(e))