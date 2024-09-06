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


def course_creation(
    org,
    number,
    run,
    display_name,
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
    url = f"{CMS_HOST}/api/ibl/manage/course"
    print(url)

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

    if response.status_code == 201 or response.status_code == 200:
        print("Course created successfully.")
        return response.json()
    else:
        print(
            f"Failed to create course. Status code: {response.status_code}, Response: {response.text}"
        )
        return None


def create_or_update_program(
    org,
    program_id,
    name=None,
    slug=None,
    program_type=None,
    course_list=None,
    access_token=None,
):
    """
    Create or Update a Program in edX or Manager based on the org parameter.

    :param org: Platform org ('edx' for edX, 'manager' for Manager)
    :param program_id: Program ID
    :param name: Program name (optional)
    :param slug: Program slug (optional)
    :param program_type: Program type (numeric code, optional)
    :param course_list: Array of dicts with course_id keys (optional)
    :return: Response status and message
    """
    print("Creating or updating program...")

    # Determine the URL based on the org
    print("Creating course...")
    url = f"{MANAGER_URL}/api/catalog/programs/"
    print(url)

    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOKEN_URL,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."

    # Prepare the payload
    payload = {
        "program_id": program_id,
        "org": org,
        "name": name,
        "slug": slug,
        "program_type": program_type,
        "course_list": course_list,
    }
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    print(payload)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return f"Program {'updated' if response.status_code == 200 else 'created'} successfully."
    else:
        return f"Failed to create or update program. Status code: {response.status_code}, Response: {response.text}"


def create_or_update_pathway(
    username, user_id, pathway_id, name, path, data, access_token=None
):
    """
    Create or Update a Pathway in edX or Manager based on the org parameter.

    :param org: Platform org ('edx' for edX, 'manager' for Manager)
    :param username: Username associated with the pathway (optional if user_id is provided)
    :param user_id: User ID associated with the pathway (optional if username is provided)
    :param pathway_id: Pathway ID
    :param name: Pathway name
    :param path: List of path objects
    :param data: Additional data for the pathway
    :param access_token: Access token for authentication (optional)
    :return: Response status and message
    """
    print("Creating or updating pathway...")

    # Determine the URL based on the org
    url = f"{MANAGER_URL}/api/catalog/pathways/"
    print(url)

    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOKEN_URL,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."

    # Prepare the payload
    payload = {
        "username": username,
        "user_id": user_id,
        "pathway_id": pathway_id,
        "name": name,
        "path": path,
        "data": data,
    }
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    print(payload)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        return "Pathway created or updated successfully."
    else:
        return f"Failed to create or update pathway. Status code: {response.status_code}, Response: {response.text}"


def create_or_update_resource(name, url, resource_type, data, access_token=None):
    """
    Create or Update a Resource in Manager.

    :param name: Resource name
    :param url: Resource URL
    :param resource_type: Type of the resource (e.g., 'book', 'video')
    :param data: Additional data for the resource
    :param access_token: Access token for authentication (optional)
    :return: Response status and message
    """
    print("Creating or updating resource...")

    # Manager URL for resource creation or update
    url = f"{MANAGER_URL}/api/catalog/resources/"

    if access_token is None:
        access_token = get_access_token(
            url=MANAGER_ACCESS_TOKEN_URL,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )
        if access_token is None:
            return "Failed to obtain access token."

    # Prepare the payload
    payload = {"name": name, "url": url, "resource_type": resource_type, "data": data}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        return "Resource created or updated successfully."
    else:
        return f"Failed to create or update resource. Status code: {response.status_code}, Response: {response.text}"


# inoder to create courses please update the request data with the appropriate values
course_creations = course_creation(
    "main", "COURSE2024DUMMY", "T1_01", "Sample API Created Course"
)
print(course_creations)

# inoder to create programs please update the request data with the appropriate values
program_creations = create_or_update_program(
    "main", "PROGRAM2024DUMMY", "Sample API Created Program", "sample-api-created-program-dummy"
)
print(program_creations)

# inoder to create pathways please update the request data with the appropriate values
pathway_creations = create_or_update_pathway(
    "johndoe_111222",
    None,
    "PATHWAY2024DUMMY",
    "Sample API Created Pathway Dummy",
    [],
    {"key": "test data"},
)
print(pathway_creations)

# inoder to create resources please update the request data with the appropriate values
resource_creations = create_or_update_resource(
    "Sample API Created Resource",
    "https://www.example.com",
    "book",
    {"key": "test data"},
)
print(resource_creations)

def update_xblock(locator, course_key, category, metadata=None, display_name=None, data=None, access_token=None):
    """
    Update an Xblock
    POST api/v1/ibl/xblock/update
    """
    print("Updating xblock...")
    url = f"{CMS_HOST}/api/v1/ibl/xblock/update"

    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return

    payload = {
        "locator": locator,
        "courseKey": course_key,
        "category": category,
    }
    if metadata:
        payload["metadata"] = metadata
    if display_name:
        payload["display_name"] = display_name
    if data:
        payload["data"] = data

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Xblock updated successfully.")
        return response.json()
    else:
        print(f"Failed to update xblock. Status code: {response.status_code}, Response: {response.text}")
        return None

def get_xblock_details(locator, access_token=None):
    """
    Get Xblock Details
    GET api/v1/ibl/xblock/get-details
    """
    print("Getting xblock details...")
    url = f"{CMS_HOST}/api/v1/ibl/xblock/get-details"

    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return

    payload = {"locator": locator}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers, params=payload)

    if response.status_code == 200:
        print("Xblock details retrieved successfully.")
        return response.json()
    else:
        print(f"Failed to get xblock details. Status code: {response.status_code}, Response: {response.text}")
        return None

def publish_unit(locator, access_token=None):
    """
    Publish Unit
    POST api/v1/ibl/xblock/publish
    """
    print("Publishing unit...")
    url = f"{CMS_HOST}/api/v1/ibl/xblock/publish"

    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return

    payload = {"locator": locator}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Unit published successfully.")
        return response.json()
    else:
        print(f"Failed to publish unit. Status code: {response.status_code}, Response: {response.text}")
        return None

def create_xblock(parent_locator, category, display_name=None, boilerplate=None, position=None, access_token=None):
    """
    Create Xblock (Generic)
    POST api/v1/ibl/xblock/create
    """
    print("Creating xblock...")
    url = f"{CMS_HOST}/api/v1/ibl/xblock/create"

    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return

    payload = {
        "parent_locator": parent_locator,
        "category": category,
    }
    if display_name:
        payload["display_name"] = display_name
    if boilerplate:
        payload["boilerplate"] = boilerplate
    if position:
        payload["position"] = position

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Xblock created successfully.")
        return response.json()
    else:
        print(f"Failed to create xblock. Status code: {response.status_code}, Response: {response.text}")
        return None

def create_component(parent_locator, problem_type, data=None, metadata=None, display_name=None, boilerplate=None, position=None, access_token=None):
    """
    Create Component (Multiple-choice, Video, HTML, SCORM)
    POST api/v1/ibl/xblock/component/create
    """
    print(f"Creating {problem_type} component...")
    url = f"{CMS_HOST}/api/v1/ibl/xblock/component/create"

    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return

    payload = {
        "parent_locator": parent_locator,
        "problem_type": problem_type,
    }
    if data:
        payload["data"] = data
    if metadata:
        payload["metadata"] = metadata
    if display_name:
        payload["display_name"] = display_name
    if boilerplate:
        payload["boilerplate"] = boilerplate
    if position:
        payload["position"] = position

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"{problem_type.capitalize()} component created successfully.")
        return response.json()
    else:
        print(f"Failed to create {problem_type} component. Status code: {response.status_code}, Response: {response.text}")
        return None

def update_scorm_component(usage_key_string, display_name, weight, fullscreen_on_launch, has_score, height, file=None, handler="studio_submit", suffix=None, access_token=None):
    """
    Update Scorm Component
    POST api/v1/ibl/ibl_edx_scorm/update
    """
    print("Updating SCORM component...")
    url = f"{CMS_HOST}/api/v1/ibl/ibl_edx_scorm/update"

    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return

    payload = {
        "display_name": display_name,
        "weight": weight,
        "fullscreen_on_launch": fullscreen_on_launch,
        "handler": handler,
        "usage_key_string": usage_key_string,
        "has_score": has_score,
        "height": height,
    }
    if file:
        payload["file"] = file
    if suffix:
        payload["suffix"] = suffix

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("SCORM component updated successfully.")
        return response.json()
    else:
        print(f"Failed to update SCORM component. Status code: {response.status_code}, Response: {response.text}")
        return None

def add_lti_passport(course_key, lti_passport, access_token=None):
    """
    Add Lti Passport to a Course
    POST api/v1/ibl/course/add_lti_passport
    """
    print("Adding LTI passport to course...")
    url = f"{CMS_HOST}/api/v1/ibl/course/add_lti_passport"

    if access_token is None:
        access_token = get_access_token()
        if access_token is None:
            return

    payload = {
        "courseKey": course_key,
        "lti_passport": lti_passport,
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("LTI passport added successfully.")
        return response.json()
    else:
        print(f"Failed to add LTI passport. Status code: {response.status_code}, Response: {response.text}")
        return None

# Example usage of new functions
if __name__ == "__main__":
    # ... (rest of the code remains unchanged) ...
