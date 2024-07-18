import json

import requests

# Manager base url to be changed
BASE_URL = "https://base.manager.<DOMAIN>/"

# user details to be changed
TENANT = ""
USERNAME = ""
ACCESS_TOKEN = ""  # this must be a tenant api key

# THIS ENDPOINT ALLOWS ONLY TENANT ADMINS TO CREATE MENTORS.


def index_document_from_file():
    """
    Index file document for a particular mentor.
    """
    pathway = ""  # The pathway here should match the name of the mentor for which the document is being indexed
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


def index_document_from_url():
    """
    Index url document for a particular mentor.

    """
    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    pathway = ""  # The pathway here should match the name of the mentor for which the document is being indexed
    url = "" # url of the webpage you want indexed.
    data = {
        "type": "webcrawler",
        "pathway": pathway,
        "url": url,
    }
    response = requests.post(
        f"{BASE_URL}api/ai-index/orgs/{TENANT}/users/{USERNAME}/documents/train/",
        headers=headers,
        data=json.dumps(data),
    )

    if response.ok:
        print(response.json())

    else:
        print(response.status_code)
        print(response.text)
