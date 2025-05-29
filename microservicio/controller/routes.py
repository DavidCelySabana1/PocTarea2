from fastapi import APIRouter, Depends
from facade.api_facade import get_github_user_info
from utils.token_validator import validate_token

router = APIRouter()

@router.get("/github-user/{username}")
def github_user(username: str, user=Depends(validate_token)):
    print(f"Usuario autenticado: {user}", flush=True)
    print(f"Obteniendo información de GitHub para el usuario: {username}", flush=True)
    return get_github_user_info(username)