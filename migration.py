import json

import requests

# Base URL for the Manager, LMS and CMS to be updated
MANAGER_URL = "https://base.manager.<>"
LMS_HOST = "https://learn.<>"
CMS_HOST = "https://studio.learn.<>"

# Client ID and Client Secret for the LMS to be updated
EDX_CLIENT_ID = "some client id"
EDX_CLIENT_SECRET = "some client secret"

# Client ID and Client Secret for the Manager to be updated
MANAGER_CLIENT_ID = "some client id"
MANAGER_CLIENT_SECRET = (
    "some client secret"
)
EDX_ACCESS_TOKEN_URL = f"{LMS_HOST}/oauth2/access_token/"
MANAGER_ACCESS_TOKEN_URL = f"{MANAGER_URL}/oauth/token/"
COURSE_CREATION_URL = f"{CMS_HOST}/api/ibl/manage/course"
USER_CREATION_URL = f"{LMS_HOST}/api/ibl/users/manage/"
SKILLS_URL = f"{MANAGER_URL}/api/catalog/skills/"

# Check in the list of issuers the platforms in your manager : <manager_url>/admin/dl_cred_app/issuer/
CRED_ISSUER_PLATFORM = "ibl" # This is the org to which the issuer is linked


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


def course_creation(
    org,
    number,
    run,
    display_name,
    url=COURSE_CREATION_URL,
    source_course_key=None,
    access_token=None,
):
    """
    Course Creation Endpoint
    POST /api/ibl/manage/course

    Allows the user to create a course, or launch course reruns. The user sending the request must be an admin of the organization or global staff.

    Params
    org (string)
    Course org
    number (string)
    Course number
    run (string)
    Course run
    display_name (string)
    Initial display name for the course
    source_course_key (string, optional)
    The course ID that the rerun is based on
    Use this only when creating a course rerun

    """
    print("Creating course...")
    print(url)
    access_token = "p40gw5NnAQEs83sJX2tWGAbwCwmZOi"
    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return

    payload = {
        "org": org,
        "number": number,
        "run": run,
        "display_name": display_name,
    }

    if source_course_key:
        payload["source_course_key"] = source_course_key

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


    response = requests.post(url, headers=headers, json=payload)

    print(response.text)


def user_creation(username, email, password, url=USER_CREATION_URL, access_token=None):
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


def create_or_update_skill(name, slug, data, url=SKILLS_URL, access_token=None):
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
    print(url)
    access_token = "Qt61EryPFyZw2B60qlETn5DWwLJP6F"
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


def get_issuer_from_org(org="main", default_org="main", access_token=None):
    """
    Create an issuer for an organization.

    Parameters:
    - url: The base URL of the API endpoint for creating issuers.
    - access_token: The OAuth2 access token for authorization.
    - issuer_data: A dictionary containing the issuer data.

    Returns:
    - A message indicating the success or failure of the operation, or the response data on success.
    """
    print("Creating issuer...")
    url = f"{MANAGER_URL}/api/credentials/orgs/{default_org}/users/ibl-admin/issuers/{org}"
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
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 201:
        return "Issuer created successfully.", response.json()
    elif response.status_code == 400:
        return "Failed to create issuer. Reason: Bad request.", None
    elif response.status_code == 401:
        return "Failed to create issuer. Reason: Invalid token.", None
    else:
        return f"Unexpected error. Status code: {response.status_code}, Response: {response.text}", None


def issue_credential_single(entity_id, recipient_email, recipient_identity, course, metadata, default_org="main", url=MANAGER_URL, access_token=None):
    """
    Issue a credential to a single user.

    Parameters:
    - entity_id: The ID of the entity issuing the credential.
    - recipient_email: The email of the recipient.
    - recipient_identity: The username of the recipient.
    - course: The course ID.
    - metadata: Additional metadata for the credential.
    - url: The base URL of the API endpoint.
    - access_token: The OAuth2 access token for authorization.

    Returns:
    - A message indicating the success or failure of the operation, or the response data on success.
    """
    print("Issue credential...")
    url = f"{MANAGER_URL}/api/credentials/orgs/{default_org}/users/ibl-admin/{entity_id}/assertions/"
    print(url)

    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOKEN_URL,
            client_id=MANAGER_CLIENT_ID,
            client_secret=MANAGER_CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."

    credential_data = {
        "recipient": {
            "email": recipient_email,
            "identity": recipient_identity
        },
        "course": course,
        "metadata": metadata
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(credential_data))

    if response.status_code == 201:
        return "Issuer issued successfully.", response.json()
    elif response.status_code == 400:
        return "Failed to issue credential. Reason: Bad request.", None
    elif response.status_code == 401:
        return "Failed to issue credential. Reason: Invalid token.", None
    else:
        return f"Unexpected error. Status code: {response.status_code}, Response: {response.text}", None


def create_credential(credential_data, issuer_platform=CRED_ISSUER_PLATFORM, access_token=None):
    """
    Create a credential.

    Parameters:
    - url: The base URL of the API endpoint.
    - access_token: The OAuth2 access token for authorization.
    - credential_data: A dictionary containing the credential data.

    Returns:
    - A message indicating the success or failure of the operation, or the response data on success.
    """
    print("Creating credential...")
    url = f"{MANAGER_URL}/api/credentials/orgs/{issuer_platform}/users/ibl-admin/"
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
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(credential_data))

    if response.status_code == 201 or response.status_code == 200:
        return "Credential created successfully.", response.json()
    elif response.status_code in [400, 500]:
        return f"Failed to create credential. Status code: {response.status_code}, Response: {response.text}", None
    else:
        return f"Unexpected error. Status code: {response.status_code}, Response: {response.text}", None


# Example usage
# Functions can be imported from another script that reads data from a CSV and passes them into the functions to be called in a loop

# In order to create users please update the request data with the appropriate values
user_creations = user_creation(
    "johndoe_111444", "johndoe+111444@iblai.tech", "somepassword4657"
)
print(user_creations)

# In order to create courses please update the request data with the appropriate values
course_creations = course_creation("main", "COURSE2024", "T1_01", "Sample API Created Course")
print(course_creations)

# Pass in the org that you want to get the issuer from
result, response_data = get_issuer_from_org("main")
print(result)
print(response_data)

# Issue a single credential, update the request data with the appropriate values
entity_id = "HaJsHrdUSL6QIJS5OEHcPw" # You can get a credential entity_id from looking at any credential in the manager at : /admin/dl_cred_app/credential/
recipient_email = "johndoe+111444@example.com"
recipient_identity = "johndoe_111444"
course = "course-v1:main+COURSE2024+T1_01"
metadata = {}

message, response = issue_credential_single(entity_id, recipient_email, recipient_identity, course, metadata)
print(message)
if response:
    print(response)

# In order to create skills please update the request data with the appropriate values
data = {"test-data": "this is some cool java data"}
create_or_update_skills = create_or_update_skill("Java", "java", data)
print(create_or_update_skills)

# In order to create credentials please update the request data with the appropriate values
credential_data = {
    "issuer": "ll_PY1VCR1CH3-4-3KTgLA",
    "name": "API Credential",
    "description": "Description of the API Credential",
    "iconImage": "https://store.credentials.dev.ibl.ai/media/uploaded_images/BadgeImage.jpg",
    "thumbnailImage": "https://store.credentials.dev.ibl.ai/media/uploaded_images/BadgeImage.jpg",
    "backgroundImage": "https://store.credentials.dev.ibl.ai/media/uploaded_images/BadgeImage.jpg",
    "credentialType": "MICROCREDENTIAL",
    "tags": [],
    "criteriaNarrative": "Complete all required activities.",
    "criteriaUrl": "https://example.com/criteria",
    "public": False,
    "metadata": {
        "price": 200
    },
    "expires": {
        "duration": "months",
        "amount": 6
    },
    "courses": ["course-v1:main+COURSE2024+T1_01"],
    "programs": [],
    "html_template": "<h1>Welcome to IBL Credentials</h1>",
    "css_template": ""
}

result, response_data = create_credential(credential_data)
print(result)
print(response_data)
