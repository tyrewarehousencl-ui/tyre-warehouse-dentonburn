import os
from dotenv import load_dotenv
from dvla_auth import DVLAAuthClient

load_dotenv()

DVLA_USERNAME = os.getenv("DVLA_USERNAME")
DVLA_PASSWORD = os.getenv("DVLA_PASSWORD")
DVLA_API_KEY = os.getenv("DVLA_API_KEY")
DVLA_ENV = os.getenv("DVLA_ENV", "UAT")

if __name__ == "__main__":
    print("--- Initializing DVLA Auth Client ---")
    client = DVLAAuthClient(
        username=DVLA_USERNAME,
        password=DVLA_PASSWORD,
        api_key=DVLA_API_KEY,
        env=DVLA_ENV,
    )

    try:
        headers = client.get_auth_headers()
        print("✓ Authentication successful!")
        print(f"Generated Header Keys: {list(headers.keys())}")
        print(f"JWT Token snippet: {headers['Authorization'][:25]}...")
    except Exception as e:
        print(f"❌ Error: {e}")