from app.ConfigLoader import ConfigLoader
from app.WorkflowManager import WorkflowManager
from app.Caller import Caller
from typing import List, Dict, Any
from app.models.RequestModel import RequestModel, Process, DataItem


class Orchestrator:
    def __init__(self, workflow_manager: WorkflowManager, caller: Caller, config_loader: ConfigLoader):
        self.workflow_manager = workflow_manager
        self.caller = caller
        self.config_loader = config_loader

    def start_process(self, data: RequestModel) -> List[Dict[str, Any]]:
        results = []

        for process in data.processes:
            process_name = process.name
            params = process.params

            for data_item in params.data:
                try:
                    url_params = {
                        "country": data_item.country,
                        "resource": data_item.resource,
                        "stop": data_item.stop,
                    }
                    data_payload = {}
                    for step in self.workflow_manager.steps:
                        service_url = self.workflow_manager.get_step(step["name"])["service_url"]
                        route = step["route"]
                        method = step["method"]
                        url = service_url + route
                        url = url.format(**url_params)
                        if "headers" in step:
                            headers = step["headers"]
                        else:
                            headers = {}

                        try:
                            response = self.caller.call_microservice(headers ,method, url, data_payload)
                            if step["response_type"] == "application/json":
                                data_payload = response.json()
                            else:
                                data_payload = response.text

                        except Exception as e:
                            results.append({
                                "process": process_name,
                                "data": data_payload,
                                "status": "failed",
                                "error": f"Error at {step['name']}: {str(e)}"
                            })
                            break
                    else:
                        results.append({
                            "process": process_name,
                            "data": data_payload,
                            "status": "success"
                        })

                except Exception as e:
                    results.append({
                        "process": process_name,
                        "data": {
                            "country": data_item.country,
                            "resource": data_item.resource,
                            "stop": data_item.stop,
                        },
                        "status": "error",
                        "error": str(e)
                    })

        return results
