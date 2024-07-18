from typing import Literal
import requests

# Base URL for the Manager, LMS and CMS to be updated
MANAGER_URL = "https://base.manager.example.com"
LMS_HOST = "https://learn.example.com"
CMS_HOST = "https://studio.learn.example.com"

EDX_ACCESS_TOKEN_URL = f"{LMS_HOST}/oauth2/access_token/"
MANAGER_ACCESS_TOKEN_URL = f"{MANAGER_URL}/oauth/token/"

# Client ID and Client Secret for the LMS to be updated

# Get CLIENT_ID and CLIENT_SECRET from the Django admin panel : LMS_HOST/admin/ibl_api_auth/oauthcredentials/
CLIENT_ID = "replace_with_client_id"
CLIENT_SECRET = "replace_with_client_secret"


def get_access_token(
    url=EDX_ACCESS_TOKEN_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET
):
    """
    Get Access Token
    POST /oauth2/access_token

    """
    print("Getting access token...")
    print(url)
    payload = f"client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        print(
            f"Failed to obtain access token. Status code: {response.status_code}, Response: {response.text}"
        )
        return None


def create_bot(
    name,
    client_id: str,
    secret_key: str,
    app_token: str,
    verification_token: str,
    provider: Literal[
        "slack",
        "webex",
        "whatsapp",
        "discord",
    ],
    config: dict,
    tenant: str,
    access_token: str | None = None,
):

    print("Creating or updating role...")
    url = f"{MANAGER_URL}/api/ai-bot/v1/bots/{tenant}/"
    print(url)

    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOKEN_URL,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "tenant": tenant,
        "name": name,
        "client_id": client_id,
        "client_secret": secret_key,
        "app_token": app_token,
        "verification_token": verification_token,
        "provider": provider,
        "config": config,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        return "Bot created or updated successfully."
    else:
        print(
            f"Failed to create or update bot. Status code: {response.status_code}, Response: {response.text}"
        )
        return None


def create_bot_command(command: str, mentor_id: int, bot_id: int, access_token=None):
    print("Creating or updating bot command...")
    url = f"{MANAGER_URL}/api/ai-bot/v1/botcommands/"
    print(url)

    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOKEN_URL,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "command": command,
        "mentor": mentor_id,
        "bot": bot_id,
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        return "Bot created or updated successfully."
    else:
        print(
            f"Failed to create or update bot. Status code: {response.status_code}, Response: {response.text}"
        )
        return None
