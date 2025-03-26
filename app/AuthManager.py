import requests
from dotenv import load_dotenv
import os
from typing import Dict

# AuthManager.py
class AuthManager:
    def login(self, credentials):
        try:
            data = {
                'client_id': os.getenv('KEYCLOAK_CLIENT_ID'),
                'client_secret': os.getenv('KEYCLOAK_CLIENT_SECRET'),
                'grant_type': 'password',
                'username': credentials["username"],
                'password': credentials["password"]
            }


            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            req = requests.post(os.getenv('KEYCLOAK_URL'), data=data, headers=headers)
            req.raise_for_status()
            return req.json()

        except Exception as e:
            return {"error": str(e)}