import json
import requests

# Manager base url to be changed
BASE_URL = "https://base.manager.<DOMAIN>/"

# user details to be changed
TENANT = ""
USERNAME = ""
ACCESS_TOKEN = ""  # this must be a tenant api key

# THIS ENDPOINT ALLOWS ONLY TENANT ADMINS TO CREATE LLM CREDENTIALS.



# Details of the llm credentials to be created.
data = {
    "name": "openai",
    "value": {"key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"},
    "platform": "main",
}


def llm_credential_creation(data):
    """
    Create llm credential for a tenant via the API.

    """
    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        f"{BASE_URL}api/ai-account/orgs/{TENANT}/credential/",
        headers=headers,
        data=json.dumps(data),
    )

    if response.ok:
        print(response.json())

    else:
        print(response.status_code)
        print(response.text)



def get_llm_credentials():
    """
    Get llm credential for a tenant via the API.

    """
    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        f"{BASE_URL}api/ai-account/orgs/{TENANT}/credential/",
        headers=headers,
    )

    if response.ok:
        print(response.json())

    else:
        print(response.status_code)
        print(response.text)