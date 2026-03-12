import requests
from config import BACKEND_URL


def login(params):
    response = requests.post(
        f"{BACKEND_URL}/api/login",
        json=params
    )
    return response.json()
