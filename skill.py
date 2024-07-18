import requests

# Base URL for the Manager, LMS and CMS to be updated
MANAGER_URL = "https://base.manager.example.com"
LMS_HOST = "https://learn.example.com"
CMS_HOST = "https://studio.learn.example.com"

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


def create_or_update_skill(name, slug, data, access_token=None):
    """
    Create or update a skill.

    Parameters:
    - access_token: The OAuth2 access token for authorization.
    - name: The name of the skill.
    - slug: The slug for the skill.
    - data: A dictionary containing additional data for the skill.

    Returns:
    - A message indicating the success or failure of the operation.
    """
    print("Creating or updating skill...")
    url = f"{MANAGER_URL}/api/catalog/skills/"
    print(url)
    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOKEN_URL,
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

    if response.status_code == 201 or response.status_code == 200:
        return "Skill created or updated successfully."
    elif response.status_code == 400:
        return "Failed to create or update skill. Reason: Invalid params."
    elif response.status_code == 500:
        return "Failed to create or update skill. Reason: Server error."
    else:
        return f"Failed to create or update skill. Status code: {response.status_code}, Response: {response.text}"


def create_or_update_desired_skill(
    user_id=None, username=None, skills=None, data=None, access_token=None
):
    """
    Create or update desired skills for a user.

    Parameters:
    - access_token: The OAuth2 access token for authorization.
    - user_id: The user's ID.
    - username: The username of the user.
    - skills: A list of skill names.
    - data: A dictionary containing additional data for the desired skills.

    Returns:
    - A message indicating the success or failure of the operation.
    """
    print("Creating or updating desired skills...")
    url = f"{MANAGER_URL}/api/catalog/skills/desired/"
    print(url)
    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOKEN_URL,
            client_id=MANAGER_CLIENT_ID,
            client_secret=MANAGER_CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"user_id": user_id, "username": username, "skills": skills, "data": data}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return "Desired skills created or updated successfully."
    elif response.status_code == 400:
        return "Failed to create or update desired skills. Reason: Invalid params."
    elif response.status_code == 500:
        return "Failed to create or update desired skills. Reason: Server error."
    else:
        return f"Failed to create or update desired skills. Status code: {response.status_code}, Response: {response.text}"


def create_or_update_reported_skill(
    user_id=None, username=None, skills=None, data=None, access_token=None
):
    """
    Create or update reported skills for a user.

    Parameters:
    - access_token: The OAuth2 access token for authorization.
    - user_id: The user's ID.
    - username: The username of the user.
    - skills: A list of skill names.
    - data: A dictionary containing additional data for the reported skills.

    Returns:
    - A message indicating the success or failure of the operation.
    """
    print("Creating or updating reported skills...")
    url = f"{MANAGER_URL}/api/catalog/skills/reported/"
    print(url)

    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOKEN_URL,
            client_id=MANAGER_CLIENT_ID,
            client_secret=MANAGER_CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"user_id": user_id, "username": username, "skills": skills, "data": data}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return "Reported skills created or updated successfully."
    elif response.status_code == 400:
        return "Failed to create or update reported skills. Reason: Invalid params."
    elif response.status_code == 500:
        return "Failed to create or update reported skills. Reason: Server error."
    else:
        return f"Failed to create or update reported skills. Status code: {response.status_code}, Response: {response.text}"


# Example usage

# inoder to create skills please update the request data with the appropriate values
data = {"test-data": "this is some cool java data"}
create_or_update_skills = create_or_update_skill("Java", "java", data)
print(create_or_update_skills)

# create or update desired skills
data = {"beep": 10}
skills = ["Test Skill"]
create_or_update_desired_skills_response = create_or_update_desired_skill(
    user_id=17, skills=skills, data=data
)
print(create_or_update_desired_skills_response)

# create or update reported skills
data = {"beep": 10}
skills = ["Test Skill"]
create_or_update_reported_skills_response = create_or_update_reported_skill(
    user_id=17, skills=skills, data=data
)
print(create_or_update_reported_skills_response)
