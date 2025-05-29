import os
from dotenv import load_dotenv
from pathlib import Path

# Sube dos niveles desde utils/token_handler.py → microservicio/config/.env
dotenv_path = Path(__file__).resolve().parents[1] / "config" / ".env"
load_dotenv(dotenv_path)

def get_github_token():
    return os.getenv("GITHUB_TOKEN", "")
