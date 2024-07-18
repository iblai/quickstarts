import requests

# Base URL for the Manager, LMS and CMS to be updated
MANAGER_URL = "https://base.manager.iblai.ai"
LMS_HOST = "https://learn.iblai.ai"
CMS_HOST = "https://studio.learn.iblai.ai"

# Client ID and Client Secret for the LMS to be updated
EDX_CLIENT_ID = "client_id"
EDX_CLIENT_SECRET = "client_secret"

# Client ID and Client Secret for the Manager to be updated
MANAGER_CLIENT_ID = "client_id"
MANAGER_CLIENT_SECRET = "client_secret"

EDX_ACCESS_TOKEN_URL = f"{LMS_HOST}/oauth2/access_token/"
MANAGER_ACCESS_TOKEN_URL = f"{MANAGER_URL}/oauth/token/"


def get_access_token(
    url=EDX_ACCESS_TOKEN_URL, client_id=EDX_CLIENT_ID, client_secret=EDX_CLIENT_SECRET
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

def launch_tenant(username, email, password, firstname, lastname, role, key, name, access_token=None):
    """
    Launches a new tenant on the platform.

    :param username: Platform admin username
    :param email: Platform admin email
    :param password: Platform admin password
    :param firstname: Platform admin firstname
    :param lastname: Platform admin lastname
    :param role: Platform admin role in organization (based on edX user roles)
    :param key: Platform key
    :param name: Platform name
    :return: Response from the API
    """
    print("Launching tenant...")
    url = f"{MANAGER_URL}/api/service/launch/tenant/"
    print(url)
    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOKEN_URL,
            client_id=MANAGER_CLIENT_ID,
            client_secret=MANAGER_CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."

    payload = {
        "username": username,
        "email": email,
        "password": password,
        "firstname": firstname,
        "lastname": lastname,
        "role": role,
        "key": key,
        "name": name
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        print("Tenant launched successfully.")
        return response.json()
    else:
        print(f"Failed to launch tenant. Status code: {response.status_code}, Response: {response.text}")
        return None

# Sample call to launch_tenant function
launch_tenant_response = launch_tenant(
    username="adminuser",
    email="admin@example.com",
    password="securepassword123",
    firstname="Admin",
    lastname="User",
    role="org-instructor",
    key="uniqueplatformkey",
    name="My New Platform"
)

print(launch_tenant_response)
