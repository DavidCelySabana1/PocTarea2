
import os
# Crear el archivo docker-compose.yml
docker_compose_content = '''
version: '3.8'

services:
  keycloak:
    image: quay.io/keycloak/keycloak:latest
    command: start-dev
    environment:
      - KEYCLOAK_ADMIN=admin
      - KEYCLOAK_ADMIN_PASSWORD=admin
    ports:
      - "8080:8080"

  app:
    build: .
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    working_dir: /app
    depends_on:
      - keycloak
    env_file:
      - config/.env
'''

docker_compose_path = f'C://Users//robinsoncelri//Documents//GitHub//Avi-Dev//PocMicroservicios//microservicio//docker-compose.yml'
with open(docker_compose_path, "w") as f:
    f.write(docker_compose_content.strip())


# Restaurar la estructura del proyecto
base_path = f'C://Users//robinsoncelri//Documents//GitHub//Avi-Dev//PocMicroservicios//microservicio'

structure = {
    "controller": {
        "routes.py": '''
from fastapi import APIRouter, Depends
from facade.api_facade import get_github_user_info
from utils.token_validator import validate_token

router = APIRouter()

@router.get("/github-user/{username}")
def github_user(username: str, user=Depends(validate_token)):
    return get_github_user_info(username)
'''
    },
    "facade": {
        "api_facade.py": '''
from service.github_service import fetch_user_info

def get_github_user_info(username: str):
    return fetch_user_info(username)
'''
    },
    "service": {
        "github_service.py": '''
import requests
from utils.token_handler import get_github_token

def fetch_user_info(username: str):
    token = get_github_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"https://api.github.com/users/{username}", headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": "Usuario no encontrado", "status": response.status_code}
'''
    },
    "utils": {
        "token_handler.py": '''
import os

def get_github_token():
    return os.getenv("GITHUB_TOKEN", "")
''',
        "token_validator.py": '''
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests

bearer_scheme = HTTPBearer()
KEYCLOAK_JWKS_URL = "http://keycloak:8080/realms/demo-realm/protocol/openid-connect/certs"

def get_public_key():
    jwks = requests.get(KEYCLOAK_JWKS_URL).json()
    key = jwks["keys"][0]
    return jwt.construct_rsa_public_key(key)

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        public_key = get_public_key()
        payload = jwt.decode(token, public_key, algorithms=["RS256"], audience="account")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
'''
    },
    "config": {
        ".env": 'GITHUB_TOKEN=ghp_tu_token_aqui'
    },
    "": {
        "main.py": '''
from fastapi import FastAPI
from controller.routes import router as api_router

app = FastAPI()
app.include_router(api_router)
''',
        "requirements.txt": '''
fastapi
requests
python-dotenv
uvicorn
python-jose
'''
    }
}

# Crear carpetas y archivos
os.makedirs(base_path, exist_ok=True)
for folder, files in structure.items():
    dir_path = os.path.join(base_path, folder)
    os.makedirs(dir_path, exist_ok=True)
    for file_name, content in files.items():
        with open(os.path.join(dir_path, file_name), 'w') as f:
            f.write(content.strip())

