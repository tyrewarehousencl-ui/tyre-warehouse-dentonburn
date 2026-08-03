import time
import requests
from typing import Dict, Optional


class DVLAAuthClient:

    BASE_URLS = {
        "PROD": (
            "https://driver-vehicle-licensing.api.gov.uk/thirdparty-access"
        ),
        "UAT": (
            "https://uat.driver-vehicle-licensing.api.gov.uk/thirdparty-access"
        ),
    }

    def __init__(
        self,
        username: str,
        password: str,
        api_key: Optional[str] = None,
        env: str = "UAT",
    ):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.env = env.upper()

        if self.env not in self.BASE_URLS:
            raise ValueError("Environment must be either 'PROD' or 'UAT'")

        self.base_url = self.BASE_URLS[self.env]
        self.jwt_token: Optional[str] = None
        self.token_expiry_time: float = 0.0

    def is_token_valid(self) -> bool:
        return self.jwt_token is not None and time.time() < (
            self.token_expiry_time - 300
        )

    def authenticate(self) -> str:
        url = f"{self.base_url}/v1/authenticate"
        payload = {"userName": self.username, "password": self.password}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.jwt_token = data["id-token"]
            self.token_expiry_time = time.time() + 3600
            return self.jwt_token
        else:
            raise RuntimeError(
                f"Authentication failed ({response.status_code}): {response.text}"
            )

    def get_auth_headers(self) -> Dict[str, str]:
        if not self.is_token_valid():
            self.authenticate()

        if not self.api_key:
            raise ValueError(
                "API Key is missing. Set self.api_key before fetching auth headers."
            )

        return {
            "x-api-key": self.api_key,
            "Authorization": self.jwt_token,
            "Accept": "application/json",
        }