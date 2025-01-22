class WorkflowManager:
    def __init__(self, config):
        self.steps = config["steps"]
        self.services = config["services"]

    def get_step(self, step_name: str):
        for step in self.steps:
            if step["name"] == step_name:
                service_name = step.get("service")
                service = self.services.get(service_name)

                if service and "url" in service:
                    step_copy = step.copy()
                    step_copy["service_url"] = service["url"]
                    return step_copy

        raise ValueError(f"Step '{step_name}' not found in workflow.")
