import json
import requests

# Manager base url to be changed
BASE_URL = "https://base.manager.<DOMAIN>/"

# user details to be changed
TENANT = ""
USERNAME = ""
ACCESS_TOKEN = ""  # this must be a tenant api key

# THIS ENDPOINT ALLOWS ONLY TENANT ADMINS TO CREATE MENTORS.
# NOTE THAT IF YOU INDEXED DOCUMENT TO A GIVEN PATHWAY, THE MENTOR NAME MUST MATCH THE PATHWAY, OTHERWISE MENTOR WILL NOT HAVE KNOWLEDGE OF THE DOCUMENT


# Details of the mentor to be created.
mentor_data = {
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
    "proactive_prompt": """
                        Check if there are any previous chats available. If there are previous chats, mention them and offer assistance based on the last conversation. If there are no previous chats, provide a general greeting and introduce yourself with an offer to assist with writing cover letters.

                        Examples:

                        If there are previous chats:

                        Welcome back! Last time, we worked on a cover letter for [related job position]. Would you like to continue with that, or do you need help with drafting a cover letter for a product manager position?

                        If there are no previous chats:

                        Hello, I'm AI Cover Letter Helper. I aid in writing compelling cover letters. Want to draft one for a product manager position?

                        If no chat history is available do not tell the user that there is no chat history, just answer with the above instructions.
                        Do not make the response specific to a given topic, ask the user for the topic.
                        """,
    "description": "Writing compelling cover letters tailored to each job application.",
    "system_prompt": "You are a cover letter helper, aiding job seekers in writing compelling cover letters tailored to each job application. Answer quickly and concisely. Use the information below and your knowledge to answer the question. When there is no information from chat history answer normally following the the instructions. Do not mention that based on the chat history. Just answer following the instructionIntroduce yourself at the beginning of our conversation. After your initial introduction, please respond to questions or prompts naturally, without reintroducing yourself in subsequent messages.  \n\nIMPORTANT: You must ONLY reply to the current message from the user. DO NOT needlessly keep greeting or repeating messages to the user.\n\n",
}


def mentor_creation(data):
    """
    Create a new mentor via the API.

    """
    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        f"{BASE_URL}api/ai-mentor/orgs/{TENANT}/users/{USERNAME}/mentor-with-settings/",
        headers=headers,
        data=json.dumps(data),
    )
    
    if response.ok:
        print(response.json())

    else:
        print(response.status_code)
        print(response.text)

    