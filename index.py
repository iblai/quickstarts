import requests

# Manager base url to be changed
BASE_URL = "https://base.manager.<DOMAIN>/"

# user details to be changed
TENANT = ""
USERNAME = ""
ACCESS_TOKEN = ""  # this must be a tenant api key

# THIS ENDPOINT ALLOWS ONLY TENANT ADMINS TO CREATE MENTORS.

def index_document():
    """
    Index document for a particular mentor.
    """
    pathway = "", # The pathway here should match the name of the mentor which the document is being indexed
    payload = {"type": "file", "pathway": pathway}
    files = [
        (
            "file",
            (
                "space_EN.pdf",
                open("/path/to/document/space_EN.pdf", "rb"),
                "application/pdf",
            ),
        )
    ]
    headers = {"Authorization": f"Api-Token {ACCESS_TOKEN}"}
    response = requests.post(
        f"{BASE_URL}api/ai-index/orgs/{TENANT}/users/{USERNAME}/documents/train/",
        data=payload,
        files=files,
        headers=headers,
    )
    
    if response.ok:
        print(response.json())

    else:
        print(response.status_code)
        print(response.text)