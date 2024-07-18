import requests

# Base URL for the Manager, LMS and CMS to be updated
MANAGER_URL = "https://base.manager.iblai.ai"
LMS_HOST = "https://learn.iblai.ai"
CMS_HOST = "https://studio.learn.iblai.ai"

# Client ID and Client Secret for the LMS to be updated
EDX_CLIENT_ID = "client_id"
EDX_CLIENT_SECRET = "client_secrete"

# Client ID and Client Secret for the Manager to be updated
MANAGER_CLIENT_ID = "client_id"
MANAGER_CLIENT_SECRET = "client_secrete"

EDX_ACCESS_TOEKN_URL = f"{LMS_HOST}/oauth2/access_token/"
MANAGER_ACCESS_TOEKN_URL = f"{MANAGER_URL}/oauth/token/"


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
    course_id="course-v1:main+COURSE2024+T1_01", username="gipsbrian"
)
print(enroll_response)

# # Bulk enroll users
bulk_enroll_response = bulk_enroll_users(
    courses=["course-v1:main+C2+2024-04", "course-v1:main+C1+2024-04"],
    username="gipsbrian",
)
print(bulk_enroll_response)

# # Bulk enroll students
bulk_students_response = bulk_enroll_students(
    course_id="course-v1:Science+ENRGY101+2023",
    usernames=["gipsbrian", "johndoe_111222", "johndoe_111333"],
)
print(bulk_students_response)