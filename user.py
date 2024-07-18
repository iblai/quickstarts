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


def user_creation(username, email, password, access_token=None):
    """
    Create a new user via the API.

    Parameters:
        - base_url: The base URL of the API endpoint.
        - access_token: The OAuth2 access token for authorization.
        - username: The username for the new user.
        - email: The email address for the new user.
        - password: The password for the new user.
        - provider (string, optional): Supply the provider to link with.
        - tpa_uid (string, optional): Supply the social auth value to match the user with (depends on backend). Defaults to the username supplied
        - is_staff (bool, optional): Sets global staff access. Defaults to false
        - is_active (bool, optional): Set user active flag. Defaults to true on create
        - update (bool, optional): Update user details if user exists. Defaults to false (which creates a new user)
    Notes
        - Request must be made on behalf of a global staff or admin (superuser) user
        - Any parameter not supplied or of an incorrect data type (aside from username, email or update) will be ignored
        - Header authentication token should match the access token type acquired (Bearer, JWT, etc.)
        - Any errors with social auth linking will fail silently

    """
    print("Creating user...")
    url = f"{LMS_HOST}/api/ibl/users/manage/"
    print(url)

    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return "Failed to obtain access token."

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"username": username, "email": email, "password": password}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        return (
            f"User with username: {username} and email: {email} created successfully."
        )
    else:
        return f"Failed to create user. Status code: {response.status_code}, Response: {response.text}"


# Example usage
# Functions can be imported from another script that reads data from a CSV and passes them into the functions to be called in a loop

# inoder to create users please update the request data with the appropriate values
user_creations = user_creation(
    "johndoe_111555", "johndoe+111555@example.com", "somepassword4657"
)
print(user_creations)
