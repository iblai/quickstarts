import json

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
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 201:
        return "Issuer created successfully.", response.json()
    elif response.status_code == 400:
        return "Failed to create issuer. Reason: Bad request.", None
    elif response.status_code == 401:
        return "Failed to create issuer. Reason: Invalid token.", None
    else:
        return (
            f"Unexpected error. Status code: {response.status_code}, Response: {response.text}",
            None,
        )


def issue_credential_single(
    entity_id,
    recipient_email,
    recipient_identity,
    course,
    metadata,
    default_org="main",
    url=MANAGER_URL,
    access_token=None,
):
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
        "recipient": {"email": recipient_email, "identity": recipient_identity},
        "course": course,
        "metadata": metadata,
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, data=json.dumps(credential_data))

    if response.status_code == 201:
        return "Issuer issued successfully.", response.json()
    elif response.status_code == 400:
        return "Failed to issue credential. Reason: Bad request.", None
    elif response.status_code == 401:
        return "Failed to issue credential. Reason: Invalid token.", None
    else:
        return (
            f"Unexpected error. Status code: {response.status_code}, Response: {response.text}",
            None,
        )


def create_credential(credential_data, issuer_platform="ibl", access_token=None):
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
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, data=json.dumps(credential_data))

    if response.status_code == 201 or response.status_code == 200:
        return "Credential created successfully.", response.json()
    elif response.status_code in [400, 500]:
        return (
            f"Failed to create credential. Status code: {response.status_code}, Response: {response.text}",
            None,
        )
    else:
        return (
            f"Unexpected error. Status code: {response.status_code}, Response: {response.text}",
            None,
        )


# Example usage

# pass in the org that you want to get the issuer from
result, response_data = get_issuer_from_org("main")
print(result)
print(response_data)

# Issue a single credential, update the request data with the appropriate values
entity_id = "HaJsHrdUSL6QIJS5OEHcPw"  # You can get a credential entity_id from looking at any credential in the manager at : /admin/dl_cred_app/credential/
recipient_email = "johndoe+111444@example.com"
recipient_identity = "johndoe_111444"
course = "course-v1:main+COURSE2024+T1_01"
metadata = {}

message, response = issue_credential_single(
    entity_id, recipient_email, recipient_identity, course, metadata
)
print(message)
if response:
    print(response)


# inoder to create credentials please update the request data with the appropriate values
credential_data = {
    "issuer": "ll_PY1VCR1CH3-4-3KTgLA",
    "name": "API Credential",
    "description": "Description of the API Credential",
    "iconImage": "https://example.com/BadgeImage.jpg",
    "thumbnailImage": "https://example.com/BadgeImage.jpg",
    "backgroundImage": "https://example.com/BadgeImage.jpg",
    "credentialType": "MICROCREDENTIAL",
    "tags": [],
    "criteriaNarrative": "Complete all required activities.",
    "criteriaUrl": "https://example.com/criteria",
    "public": False,
    "metadata": {"price": 200},
    "expires": {"duration": "months", "amount": 6},
    "courses": ["course-v1:main+COURSE2024+T1_01"],
    "programs": [],
    "html_template": "<h1>Welcome to IBL Credentials</h1>",
    "css_template": "",
}

result, response_data = create_credential(credential_data)
print(result)
print(response_data)
