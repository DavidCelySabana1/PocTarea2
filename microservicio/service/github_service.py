import requests
from utils.token_handler import get_github_token

def fetch_user_info(username: str):
    token = get_github_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"https://api.github.com/users/{username}", headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": "Usuario no encontrado", "status": response.status_code}