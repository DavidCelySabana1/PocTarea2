from service.github_service import fetch_user_info

def get_github_user_info(username: str):
    return fetch_user_info(username)