import requests

# Base URL for the Manager, LMS and CMS to be updated
MANAGER_URL = "https://base.manager.iblai.tech"
LMS_HOST = "https://learn.iblai.tech"
CMS_HOST = "https://studio.learn.iblai.tech"

# Client ID and Client Secret for the LMS to be updated
EDX_CLIENT_ID = "TGVuV0hLWnlXMkFTOE9mRnVLdldjNW95RVRvV0Ji"
EDX_CLIENT_SECRET = (
    "VTdzaEc4S2w5d3FNMmYyanBqMTBsU3NLRU5jVGtNR0VZNmd3RE5xNXNaUkVqN1V4TjhhVFRVNjBqWkxI"
)

# Client ID and Client Secret for the Manager to be updated
MANAGER_CLIENT_ID = "TGVuV0hLWnlXMkFTOE9mRnVLdldjNW95RVRvV0Ji"
MANAGER_CLIENT_SECRET = (
    "VTdzaEc4S2w5d3FNMmYyanBqMTBsU3NLRU5jVGtNR0VZNmd3RE5xNXNaUkVqN1V4TjhhVFRVNjBqWkxI"
)

EDX_ACCESS_TOEKN_URL = f"{LMS_HOST}/oauth2/access_token/"
MANAGER_ACCESS_TOEKN_URL = f"{MANAGER_URL}/oauth/token/"
COURSE_CREATION_URL = f"{CMS_HOST}/api/ibl/manage/course"
USER_CREATION_URL = f"{LMS_HOST}/api/ibl/users/manage/"
SKILLS_URL = f"{MANAGER_URL}/api/catalog/skills/"

# Check in the list of issuers the platforms in your manager : <manager_url>/admin/dl_cred_app/issuer/
CRED_ISSUER_PLATFORM = "ibl"  # This is the org to which the issuer is linked


def get_access_token(
    url=EDX_ACCESS_TOEKN_URL, client_id=EDX_CLIENT_ID, client_secret=EDX_CLIENT_SECRET
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


def create_or_update_role(name, slug, data, access_token=None):
    """
    Create or update a role.

    Parameters:
    - name: The name of the role.
    - slug: A slug representing the role.
    - data: A dictionary containing additional data for the role.
    - access_token: The OAuth2 access token for authorization.

    Returns:
    - A message indicating the success or failure of the operation.
    """
    print("Creating or updating role...")
    url = f"{MANAGER_URL}/api/catalog/roles/"
    print(url)

    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOEKN_URL,
            client_id=MANAGER_CLIENT_ID,
            client_secret=MANAGER_CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"name": name, "slug": slug, "data": data}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        return "Role created or updated successfully."
    elif response.status_code == 400:
        return "Failed to create or update role. Reason: Invalid params."
    elif response.status_code == 500:
        return "Failed to create or update role. Reason: Server error."
    else:
        return f"Failed to create or update role. Status code: {response.status_code}, Response: {response.text}"


def create_or_update_desired_role(
    user_id=None, username=None, roles=None, data=None, access_token=None
):
    """
    Create or update desired roles for a user.

    Parameters:
    - user_id: The user's ID.
    - username: The username of the user.
    - roles: A list of role names.
    - data: A dictionary containing additional data for the desired roles.
    - access_token: The OAuth2 access token for authorization.

    Returns:
    - A message indicating the success or failure of the operation.
    """
    print("Creating or updating desired roles...")
    url = f"{MANAGER_URL}/api/catalog/roles/desired/"
    print(url)

    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOEKN_URL,
            client_id=MANAGER_CLIENT_ID,
            client_secret=MANAGER_CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"user_id": user_id, "username": username, "roles": roles, "data": data}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return "Desired roles created or updated successfully."
    elif response.status_code == 400:
        return "Failed to create or update desired roles. Reason: Invalid params."
    elif response.status_code == 500:
        return "Failed to create or update desired roles. Reason: Server error."
    else:
        return f"Failed to create or update desired roles. Status code: {response.status_code}, Response: {response.text}"


def create_or_update_reported_role(
    user_id=None, username=None, roles=None, data=None, access_token=None
):
    """
    Create or update reported roles for a user.

    Parameters:
    - user_id: The user's ID.
    - username: The username of the user.
    - roles: A list of role names.
    - data: A dictionary containing additional data for the reported roles.
    - access_token: The OAuth2 access token for authorization.

    Returns:
    - A message indicating the success or failure of the operation.
    """
    print("Creating or updating reported roles...")
    url = f"{MANAGER_URL}/api/catalog/roles/reported/"
    print(url)

    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOEKN_URL,
            client_id=MANAGER_CLIENT_ID,
            client_secret=MANAGER_CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"user_id": user_id, "username": username, "roles": roles, "data": data}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return "Reported roles created or updated successfully."
    elif response.status_code == 400:
        return "Failed to create or update reported roles. Reason: Invalid params."
    elif response.status_code == 500:
        return "Failed to create or update reported roles. Reason: Server error."
    else:
        return f"Failed to create or update reported roles. Status code: {response.status_code}, Response: {response.text}"


# Example usage

# create or update roles
data = {"beep": 10}
create_or_update_roles_response = create_or_update_role("Test Role", "test-role", data)
print(create_or_update_roles_response)


# create or update desired roles
data = {"beep": 10}
roles = ["Test Role"]
create_or_update_desired_roles_response = create_or_update_desired_role(
    user_id=17, roles=roles, data=data
)
print(create_or_update_desired_roles_response)

# create or update reported roles
data = {"beep": 10}
roles = ["Test Role"]
create_or_update_reported_roles_response = create_or_update_reported_role(
    user_id=17, roles=roles, data=data
)
print(create_or_update_reported_roles_response)
