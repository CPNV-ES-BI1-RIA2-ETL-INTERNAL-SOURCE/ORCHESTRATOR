import yaml


class ConfigLoader:
    def load_config(self, file_path: str) -> dict:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
