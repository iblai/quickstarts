# Platform Documentation

## Role Management

### Create or Update Role
- Endpoint: `{MANAGER_URL}/api/catalog/roles/`
- Method: POST
- Body:
  ```json
  {
    "name": "Role Name",
    "slug": "role-slug",
    "data": { "additional": "data" }
  }
  ```
- Response: Success message or error details

### Create or Update Desired Role
- Endpoint: `{MANAGER_URL}/api/catalog/roles/desired/`
- Method: POST
- Body:
  ```json
  {
    "user_id": 123,
    "username": "user123",
    "roles": ["Role Name"],
    "data": { "additional": "data" }
  }
  ```
- Response: Success message or error details

### Create or Update Reported Role
- Endpoint: `{MANAGER_URL}/api/catalog/roles/reported/`
- Method: POST
- Body: Same as Desired Role
- Response: Success message or error details

## Skill Management

### Create or Update Skill
- Endpoint: `{MANAGER_URL}/api/catalog/skills/`
- Method: POST
- Body:
  ```json
  {
    "name": "Skill Name",
    "slug": "skill-slug",
    "data": { "additional": "data" }
  }
  ```
- Response: Success message or error details

### Create or Update Desired Skill
- Endpoint: `{MANAGER_URL}/api/catalog/skills/desired/`
- Method: POST
- Body:
  ```json
  {
    "user_id": 123,
    "username": "user123",
    "skills": ["Skill Name"],
    "data": { "additional": "data" }
  }
  ```
- Response: Success message or error details

### Create or Update Reported Skill
- Endpoint: `{MANAGER_URL}/api/catalog/skills/reported/`
- Method: POST
- Body: Same as Desired Skill
- Response: Success message or error details

## Tenant Management

### Launch Tenant
- Endpoint: `{MANAGER_URL}/api/service/launch/tenant/`
- Method: POST
- Body:
  ```json
  {
    "username": "adminuser",
    "email": "admin@example.com",
    "password": "securepassword",
    "firstname": "Admin",
    "lastname": "User",
    "role": "org-instructor",
    "key": "uniqueplatformkey",
    "name": "My New Platform"
  }
  ```
- Response: Tenant details or error message

## Catalog Management

### Create Course
- Endpoint: `{CMS_HOST}/api/ibl/manage/course`
- Method: POST
- Body:
  ```json
  {
    "org": "org-name",
    "number": "course-number",
    "run": "course-run",
    "display_name": "Course Display Name",
    "source_course_key": "source-course-key" // Optional, for course reruns
  }
  ```
- Response: Course details or error message

### Create or Update Program
- Endpoint: `{MANAGER_URL}/api/catalog/programs/`
- Method: POST
- Body:
  ```json
  {
    "org": "org-name",
    "program_id": "program-id",
    "name": "Program Name",
    "slug": "program-slug"
  }
  ```
- Response: Success message or error details

### Create or Update Pathway
- Endpoint: `{MANAGER_URL}/api/catalog/pathways/`
- Method: POST
- Body:
  ```json
  {
    "username": "user123",
    "user_id": 123,
    "pathway_id": "pathway-id",
    "name": "Pathway Name",
    "path": [],
    "data": { "additional": "data" }
  }
  ```
- Response: Success message or error details

### Create or Update Resource
- Endpoint: `{MANAGER_URL}/api/catalog/resources/`
- Method: POST
- Body:
  ```json
  {
    "name": "Resource Name",
    "url": "https://resource-url.com",
    "resource_type": "book",
    "data": { "additional": "data" }
  }
  ```
- Response: Success message or error details

### Update XBlock
- Endpoint: `{CMS_HOST}/api/v1/ibl/xblock/update`
- Method: POST
- Body:
  ```json
  {
    "locator": "block-locator",
    "courseKey": "course-key",
    "category": "category",
    "metadata": {}, // Optional
    "display_name": "Display Name", // Optional
    "data": {} // Optional
  }
  ```
- Response: Updated XBlock details or error message

### Get XBlock Details
- Endpoint: `{CMS_HOST}/api/v1/ibl/xblock/get-details`
- Method: GET
- Query Params: `locator=block-locator`
- Response: XBlock details or error message

### Publish Unit
- Endpoint: `{CMS_HOST}/api/v1/ibl/xblock/publish`
- Method: POST
- Body:
  ```json
  {
    "locator": "block-locator"
  }
  ```
- Response: Success message or error details

### Create XBlock
- Endpoint: `{CMS_HOST}/api/v1/ibl/xblock/create`
- Method: POST
- Body:
  ```json
  {
    "parent_locator": "parent-block-locator",
    "category": "category",
    "display_name": "Display Name", // Optional
    "boilerplate": "boilerplate", // Optional
    "position": 1 // Optional
  }
  ```
- Response: Created XBlock details or error message

### Create Component
- Endpoint: `{CMS_HOST}/api/v1/ibl/xblock/component/create`
- Method: POST
- Body:
  ```json
  {
    "parent_locator": "parent-block-locator",
    "problem_type": "problem-type",
    "data": {}, // Optional
    "metadata": {}, // Optional
    "display_name": "Display Name", // Optional
    "boilerplate": "boilerplate", // Optional
    "position": 1 // Optional
  }
  ```
- Response: Created component details or error message

### Update SCORM Component
- Endpoint: `{CMS_HOST}/api/v1/ibl/ibl_edx_scorm/update`
- Method: POST
- Body:
  ```json
  {
    "usage_key_string": "usage-key",
    "display_name": "Display Name",
    "weight": 1.0,
    "fullscreen_on_launch": true,
    "has_score": true,
    "height": "400px",
    "file": "file-data", // Optional
    "handler": "studio_submit",
    "suffix": "suffix" // Optional
  }
  ```
- Response: Updated SCORM component details or error message

### Add LTI Passport to Course
- Endpoint: `{CMS_HOST}/api/v1/ibl/course/add_lti_passport`
- Method: POST
- Body:
  ```json
  {
    "courseKey": "course-key",
    "lti_passport": "lti-passport"
  }
  ```
- Response: Success message or error details

## Credential Management

### Get Issuer from Organization
- Endpoint: `{MANAGER_URL}/api/credentials/orgs/{default_org}/users/ibl-admin/issuers/{org}`
- Method: GET
- Response: Issuer details or error message

### Issue Credential (Single User)
- Endpoint: `{MANAGER_URL}/api/credentials/orgs/{default_org}/users/ibl-admin/{entity_id}/assertions/`
- Method: POST
- Body:
  ```json
  {
    "recipient": {
      "email": "user@example.com",
      "identity": "username"
    },
    "course": "course-v1:Org+Course+Run",
    "metadata": {}
  }
  ```
- Response: Credential issuance details or error message

### Create Credential
- Endpoint: `{MANAGER_URL}/api/credentials/orgs/{issuer_platform}/users/ibl-admin/`
- Method: POST
- Body:
  ```json
  {
    "issuer": "issuer-id",
    "name": "Credential Name",
    "description": "Credential Description",
    "iconImage": "https://example.com/icon.jpg",
    "thumbnailImage": "https://example.com/thumbnail.jpg",
    "backgroundImage": "https://example.com/background.jpg",
    "credentialType": "MICROCREDENTIAL",
    "tags": [],
    "criteriaNarrative": "Completion criteria",
    "criteriaUrl": "https://example.com/criteria",
    "public": false,
    "metadata": {},
    "expires": {
      "duration": "months",
      "amount": 6
    },
    "courses": ["course-v1:Org+Course+Run"],
    "programs": [],
    "html_template": "<h1>Credential Template</h1>",
    "css_template": ""
  }
  ```
- Response: Created credential details or error message

## User Management

### Create User
- Endpoint: `{LMS_HOST}/api/ibl/users/manage/`
- Method: POST
- Body:
  ```json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword"
  }
  ```
- Response: Success message or error details

Note: The following optional parameters can be included in the request body:
- `provider`: Supply the provider to link with
- `tpa_uid`: Supply the social auth value to match the user with (defaults to the username supplied)
- `is_staff`: Sets global staff access (defaults to false)
- `is_active`: Set user active flag (defaults to true on create)
- `update`: Update user details if user exists (defaults to false)

## Chat Management

### Chat with Mentor
- Endpoint: `{ASGI_BASE_URL}/ws/langflow/`
- Method: WebSocket
- Connection:
  ```json
  {
    "flow": {
      "name": "mentor-slug-or-id",
      "tenant": "tenant-name",
      "username": "username"
    },
    "session_id": "session-id",
    "token": "access-token",
    "pathway": "mentor-slug-or-id",
    "prompt": "user-question"
  }
  ```
- Response: Streaming mentor responses

Note: This endpoint allows all users to chat with mentors. When the mentor is set to anonymous, even anonymous users can chat.

## Enrollment Management

### Enroll User
- Endpoint: `{LMS_HOST}/api/ibl/enrollment/enroll/`
- Method: POST
- Body:
  ```json
  {
    "course_id": "course-v1:Org+Course+Run",
    "item_id": "item-id",
    "email": "user@example.com",
    "username": "username",
    "user_id": 123,
    "mode": "honor",
    "check_access": true
  }
  ```
- Response: Enrollment details or error message

### Bulk Enroll Users
- Endpoint: `{LMS_HOST}/api/ibl/enrollment/enroll/bulk/`
- Method: POST
- Body:
  ```json
  {
    "courses": ["course-v1:Org+Course1+Run", "course-v1:Org+Course2+Run"],
    "email": "user@example.com",
    "username": "username",
    "user_id": 123,
    "mode": "honor",
    "check_access": true
  }
  ```
- Response: Bulk enrollment details or error message

### Bulk Enroll Students
- Endpoint: `{LMS_HOST}/api/ibl/enrollment/enroll/student/bulk/`
- Method: POST
- Body:
  ```json
  {
    "course_id": "course-v1:Org+Course+Run",
    "emails": ["user1@example.com", "user2@example.com"],
    "usernames": ["username1", "username2"],
    "user_ids": [123, 456],
    "mode": "honor",
    "check_access": true
  }
  ```
- Response: Bulk student enrollment details or error message

## Mentor Management

### Create Mentor
- Endpoint: `{BASE_URL}api/ai-mentor/orgs/{TENANT}/users/{USERNAME}/mentor-with-settings/`
- Method: POST
- Headers:
  ```
  Authorization: Api-Token {ACCESS_TOKEN}
  Content-Type: application/json
  ```
- Body:
  ```json
  {
    "new_mentor_name": "AI Cover Letter Helper1",
    "display_name": "AI Cover Letter Helper1",
    "template_name": "ai-mentor",
    "slug": "ai-cover-letter-helper",
    "mentor_visibility": "viewable_by_anyone",
    "seo_tags": [],
    "metadata": {"category": "Job"},
    "marketing_conversations": [],
    "moderation_prompt": "Verify that the question involves writing compelling cover letters. Inappropriate questions include non-cover letter related inquiries or unrelated topics.",
    "proactive_message": "Hello, I'm AI Cover Letter Helper. I aid in writing compelling cover letters. Want to draft one for a product manager position?",
    "proactive_prompt": "Check if there are any previous chats available. If there are previous chats, mention them and offer assistance based on the last conversation. If there are no previous chats, provide a general greeting and introduce yourself with an offer to assist with writing cover letters.",
    "description": "Writing compelling cover letters tailored to each job application.",
    "system_prompt": "You are a cover letter helper, aiding job seekers in writing compelling cover letters tailored to each job application. Answer quickly and concisely. Use the information below and your knowledge to answer the question. When there is no information from chat history answer normally following the instructions. Do not mention that based on the chat history. Just answer following the instruction. Introduce yourself at the beginning of our conversation. After your initial introduction, please respond to questions or prompts naturally, without reintroducing yourself in subsequent messages. IMPORTANT: You must ONLY reply to the current message from the user. DO NOT needlessly keep greeting or repeating messages to the user."
  }
  ```
- Response: Mentor details or error message

Note:
- This endpoint allows only tenant admins to create mentors.
- If you indexed documents to a given pathway, the mentor name must match the pathway, otherwise the mentor will not have knowledge of the document.
- The `ACCESS_TOKEN` must be a tenant API key.
- Update the `BASE_URL`, `TENANT`, and `USERNAME` variables to match your environment.







## Bot Management

### Create Bot
- Endpoint: `{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot/`
- Method: POST
- Body:
  ```json
  {
    "name": "Bot Name",
    "client_id": "client-id",
    "client_secret": "client-secret",
    "app_token": "app-token",
    "verification_token": "verification-token",
    "provider": "slack",
    "config": {}
  }
  ```
- Response: Bot details or error message

### Update Bot
- Endpoint: `{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot/{bot_id}/`
- Method: PATCH
- Body: Same as Create Bot (partial updates allowed)
- Response: Updated bot details or error message

### Create Bot Command
- Endpoint: `{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot-commands/`
- Method: POST
- Body:
  ```json
  {
    "command": "/command",
    "mentor": 123,
    "bot": 456
  }
  ```
- Response: Command details or error message

### Update Bot Command
- Endpoint: `{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot-commands/{command_id}`
- Method: PATCH
- Body: Same as Create Bot Command (partial updates allowed)
- Response: Updated command details or error message

### Delete Bot
- Endpoint: `{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot/{bot_id}`
- Method: DELETE
- Response: Success (204) or error message

### Delete Bot Command
- Endpoint: `{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot-commands/{command_id}`
- Method: DELETE
- Response: Success (204) or error message

### List Bots
- Endpoint: `{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot/`
- Method: GET
- Response: List of bots or error message

### List Bot Commands
- Endpoint: `{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot-commands/`
- Method: GET
- Query Params: `bot={bot_id}` (optional)
- Response: List of bot commands or error message

## Authentication

For OAuth2 and SSO configurations, refer to the following URLs:

- Base Manager: https://base.manager.example.com/admin/oauth2_provider/application/
- Learning Management System:
  - OAuth2: https://learn.example.com/admin/oauth2_provider/application/
  - OpenID Connect: https://learn.example.com/admin/oidc_provider/client/
    - Fill in the following fields:
     - Enabled: True (check)
     - Name: IBL (Client Name)
     - Slug: <oauth_slug>
     - Site: <Current Site> (lms domain site)
     - Visible: True (check)
     - Skip hinted login dialog: True (check)
     - Skip registration form: True (check)
     - Skip email verification: True (check)
     - Sync learner profile data: True (check)
     - Backend name: <oauth_slug>
     - Client ID: <client_id>
     - Client Secret: <client_secret>
     - Client Type: Confidential
     - Authorization Grant Type: Authorization code
     - Redirect URIs: https://learn.example.com/auth/complete/<oauth_slug>/
     - Post Logout Redirect URIs: https://learn.example.com/
- Cross-Platform Credentials:
  - LMS to Manager: https://learn.example.com/admin/ibl_api_auth/oauthcredentials/
  - Manager to LMS: https://base.manager.example.com/admin/core/oauthcredentials/
- SSO with Third-Party Providers: https://learn.example.com/admin/third_party_auth/oauth2providerconfig/

Ensure you have the necessary permissions to access these administrative areas.