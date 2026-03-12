import requests
from config import BACKEND_URL


def get_all_stops():
    response = requests.get(
        f"{BACKEND_URL}/api/admin/route/stops"
    )
    return response.json()
