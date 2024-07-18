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


def enroll_user(
    course_id=None,
    item_id=None,
    email=None,
    username=None,
    user_id=None,
    mode="honor",
    check_access=True,
    access_token=None,
):
    """
    Enroll a registered edX user in a course.
    """
    print("Enrolling user...")
    url = f"{LMS_HOST}/api/ibl/enrollment/enroll/"
    print(url)

    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return "Failed to obtain access token."

    data = {
        "course_id": course_id,
        "item_id": item_id,
        "email": email,
        "username": username,
        "user_id": user_id,
        "mode": mode,
        "check_access": check_access,
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("User enrolled successfully")
        return response.json()
    else:
        print(
            f"Failed to enroll user. Status code: {response.status_code}, Response: {response.text}"
        )
        return response.text


def bulk_enroll_users(
    courses,
    email=None,
    username=None,
    user_id=None,
    mode="honor",
    check_access=True,
    access_token=None,
):
    """
    Bulk enroll a registered edX user in courses.
    """
    print("Bulk enrolling users...")
    url = f"{LMS_HOST}/api/ibl/enrollment/enroll/bulk/"
    print(url)

    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return "Failed to obtain access token."

    data = {
        "courses": courses,
        "email": email,
        "username": username,
        "user_id": user_id,
        "mode": mode,
        "check_access": check_access,
    }
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Users enrolled successfully")
        return response.json()
    else:
        print(
            f"Failed to enroll users. Status code: {response.status_code}, Response: {response.text}"
        )
        return response.texts


def bulk_enroll_students(
    course_id,
    emails=None,
    usernames=None,
    user_ids=None,
    mode="honor",
    check_access=True,
    access_token=None,
):
    """
    Bulk enroll students in a course.
    """
    print("Bulk enrolling students...")
    url = f"{LMS_HOST}/api/ibl/enrollment/enroll/student/bulk/"
    print(url)

    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return "Failed to obtain access token."

    data = {
        "course_id": course_id,
        "emails": emails,
        "usernames": usernames,
        "user_ids": user_ids,
        "mode": mode,
        "check_access": check_access,
    }
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Students enrolled successfully")
        return response.json()
    else:
        print(
            f"Failed to enroll students. Status code: {response.status_code}, Response: {response.text}"
        )
        return response.text


# Example usage
# Enroll a single user
enroll_response = enroll_user(
    course_id="course-v1:FM+101+001", username="gipsbrian"
)
print(enroll_response)

# # Bulk enroll users
bulk_enroll_response = bulk_enroll_users(
    courses=["course-v1:FM+101+2023", "course-v1:FinancialAcademy+FM101+2023"],
    username="gipsbrian",
)
print(bulk_enroll_response)

# # Bulk enroll students
bulk_students_response = bulk_enroll_students(
    course_id="course-v1:ACI+0003+500",
    usernames=["gipsbrian", "johndoe_111222", "johndoe_111333"],
)
print(bulk_students_response)