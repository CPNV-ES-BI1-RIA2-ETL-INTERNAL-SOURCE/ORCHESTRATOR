from fastapi import FastAPI, HTTPException

from app.Orchestrator import Orchestrator
from app.ConfigLoader import ConfigLoader
from app.WorkflowManager import WorkflowManager
from app.Caller import Caller
from app.handlers.ErrorHandler import ErrorHandler

from typing import List

from app.models.RequestModel import RequestModel

app = FastAPI()

config_loader = ConfigLoader()
caller = Caller()
workflow_manager = WorkflowManager(config_loader.load_config('config/config.yaml'))
error_handler = ErrorHandler()
orchestrator = Orchestrator(workflow_manager, caller, config_loader)


@app.post("/start-process", response_model=RequestModel)
def start_process(data: RequestModel):
    try:
        return orchestrator.start_process(data)
    except Exception as e:
        error_handler.log_error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

