from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
from jose import jwt
from jose.utils import base64url_decode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

bearer_scheme = HTTPBearer()
KEYCLOAK_JWKS_URL = "http://keycloak:8080/realms/demo/protocol/openid-connect/certs"

def get_rsa_public_key(jwk):
    e = int.from_bytes(base64url_decode(jwk['e']), 'big')
    n = int.from_bytes(base64url_decode(jwk['n']), 'big')
    public_key = rsa.RSAPublicNumbers(e, n).public_key(default_backend())
    return public_key

def get_public_key():
    jwks = requests.get(KEYCLOAK_JWKS_URL).json()
    key = jwks["keys"][0]
    return get_rsa_public_key(key)

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        public_key = get_public_key()
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience="account"
        )
        print("Token válido:", payload, flush=True)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
