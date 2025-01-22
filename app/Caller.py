import requests

class Caller:
    def call_microservice(self, method: str, url: str, data: dict) -> dict:
        try:
            if method == "GET":
                response = requests.get(url, params=data)
            elif method == "POST":
                response = requests.post(url, json=data)
                response.raise_for_status()
            else:
                raise Exception(f"Method {method} not supported")

            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling {url}: {e}")

