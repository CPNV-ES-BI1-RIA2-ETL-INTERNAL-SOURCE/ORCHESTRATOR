import httpx
import requests
from dotenv import load_dotenv
import os
from typing import Dict
from jose import jwt, JWTError


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
            url = os.getenv('KEYCLOAK_URL') + '/protocol/openid-connect/token'
            req = requests.post(url, data=data, headers=headers)
            req.raise_for_status()
            return req.json()

        except Exception as e:
            return {"error": str(e)}

    async def verify_token(self, token: str):
        keycloak_url = os.getenv('KEYCLOAK_URL')
        if not keycloak_url:
            return {"status": "invalid", "error": "KEYCLOAK_URL non défini"}

        url = os.getenv('KEYCLOAK_URL') + "/protocol/openid-connect/token/introspect"
        headers = {'Authorization': f'Bearer {token}'}

        req = requests.post(url, headers=headers)
        req.raise_for_status()
        return req.json()


