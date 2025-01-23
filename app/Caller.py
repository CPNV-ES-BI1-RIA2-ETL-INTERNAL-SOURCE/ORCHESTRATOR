import requests

class Caller:
    def call_microservice(self, header, method: str, url: str, data: dict):
        try:
            if method == "GET":
                response = requests.get(url, params=data, headers=header)
                response.raise_for_status()

            elif method == "POST":
                response = requests.post(url, json=data)
                response.raise_for_status()
            else:
                raise Exception(f"Method {method} not supported")

            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling {url}: {e}")

