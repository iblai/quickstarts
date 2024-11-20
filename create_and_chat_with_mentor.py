import asyncio
import json
from pathlib import Path
import sys
import typing as t
import asyncio
from websockets.client import connect
import logging
import httpx

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# base domain for the Data Manager service
base_url = "https://base.manager.iblai.app/"

# base domain for the websocket service
asgi_base_url = "wss://asgi.data.iblai.app"
tenant = ""  # platform key of tenant. eg: main
username = ""  # platform admin username

# this must be a platform api key
access_token = ""

mentor_name = "Test Mentor"


async def create_mentor_with_settings(data, headers):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}api/ai-mentor/orgs/{tenant}/users/{username}/mentor-with-settings/",
            headers=headers,
            data=json.dumps(data),
        )
        return response
    return response


async def create_mentor() -> dict[str, t.Any] | None:

    mentor_data = {
        "new_mentor_name": mentor_name,
        "display_name": mentor_name,
        # template mentor refers to an existing mentor that the user wants to use as a template
        # the flow of that mentor will be used along with the settings configured for the new mentor
        # we are creating to make chat possible.
        # By default the options are `ai-mentor` and `ai-agent` where
        # ai-mentor suffices for retriever based mentors
        # and ai-agent is for mentors expected to use tools.
        "template_name": "ai-mentor",
        "slug": "ai-sample-mentor",
        "mentor_visibility": "viewable_by_anyone",
        "seo_tags": [],
        "metadata": {"category": "Job"},
        "marketing_conversations": [],
        "moderation_prompt": "Verify that the question involves writing compelling cover letters. Inappropriate questions include non-cover letter related inquiries or unrelated topics.",
        "proactive_message": "Hello, I'm AI Cover Letter Helper. I aid in writing compelling cover letters. Want to draft one for a product manager position?",
        "proactive_prompt": "Please greet the user.",
        "description": "Writing compelling cover letters tailored to each job application.",
        "system_prompt": "You are a cover letter helper, aiding job seekers in writing compelling cover letters tailored to each job application. Answer quickly and concisely. Use the information below and your knowledge to answer the question. When there is no information from chat history answer normally following the the instructions. Do not mention that based on the chat history. Just answer following the instructionIntroduce yourself at the beginning of our conversation. After your initial introduction, please respond to questions or prompts naturally, without reintroducing yourself in subsequent messages.  \n\nIMPORTANT: You must ONLY reply to the current message from the user. DO NOT needlessly keep greeting or repeating messages to the user.\n\n",
    }

    headers = {
        "Authorization": f"Api-Token {access_token}",
        "Content-Type": "application/json",
    }

    mentor_creation_response = await create_mentor_with_settings(
        data=mentor_data, headers=headers
    )
    if mentor_creation_response.is_success:
        mentor_resonse_data = mentor_creation_response.json()
        logger.info("Successfully created mentor with data: %s", mentor_resonse_data)
        return mentor_resonse_data
    else:
        logger.error(
            "Failed to create mentor. Endpoint returned: %s",
            mentor_creation_response.json(),
        )
    return None


async def upload_pdf_document_to_mentor(
    mentor_name: str, file_path: str | Path
) -> dict[str, t.Any] | None:
    file_path = Path(file_path)
    payload = payload = {"type": "file", "pathway": mentor_name}
    # replace with your own file
    files = [
        (
            "file",
            (
                file_path.name,
                open(file_path, "rb"),
                "application/pdf",
            ),
        )
    ]
    headers = {"Authorization": f"Api-Token {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{base_url}api/ai-index/orgs/{tenant}/users/{username}/documents/train/",
            data=payload,
            files=files,
            headers=headers,
        )
        data = resp.json()
        if resp.is_success:
            logger.info("successfully uploaded document for training")
            logger.info("Document upload response: %s", data)
            return data
        logger.error("Failed to upload document. Endpoint returned: %s", data)
    return None


async def wait_for_document_training_to_complete(mentor_name: str) -> bool:

    headers = {"Authorization": f"Api-Token {access_token}"}
    async with httpx.AsyncClient() as client:
        while True:
            resp = await client.get(
                f"{base_url}api/ai-index/orgs/{tenant}/users/{username}/documents/pathways/{mentor_name}/",
                headers=headers,
            )

            if resp.is_success:
                data: list = resp.json()["results"]
                if all([i["is_trained"] for i in data]):
                    logger.info("All documents trained successfully")
                    return True

            # try again after 5 seconds
            logger.info("Document not trained. Trying again after 5 seconds...")
            await asyncio.sleep(5)
    return False


async def create_chat_session(mentor_name):
    # generate a session id
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{base_url}api/ai-mentor/orgs/{tenant}/users/{username}/sessions/",
            json={"mentor": mentor_name},
        )
        print(resp.json())
        session_id = resp.json().get("session_id")
        logger.info("session id: %s", session_id)
        return session_id


async def chat_with_websocket(session_id: str, mentor: str, tenant: str, username: str):
    data = {
        "flow": {
            # `name` is either the unique_id, name or slug  of the mentor in respective order of priority.
            "name": mentor,
            "tenant": tenant,
            "username": username,
        },
        "session_id": session_id,
        # `token` is the access token for the user.
        "token": access_token,
        # `pathway` is the identifier for the vector store path where documents were trained to.
        # Except for special cases, the default pathway name is the name of the mentor
        "pathway": mentor,
        # `page_content` parameter is optional. it should only be used if you intend
        # to send extra context to the mentor. This is generally the text content of the current webpage.
        "page_content": "...optional parameter to pass the content of the current web page to the mentor.",
        # `prompt` parameter is the question or message to the mentor
        "prompt": "Who is Rayana Barnawi",
    }

    ws = await connect(f"{asgi_base_url}/ws/langflow/")
    await ws.send(json.dumps(data))
    received_data = await ws.recv()
    logger.info("%s", received_data)

    # the first message after sending the payload is the status detail.
    # getting a value of `connected` means authentication was successful and
    # the user has permissions to access the said mentor
    logger.info("websocket status: %s", json.loads(received_data)["detail"])
    logger.info("Question: %s", data.get("prompt"))
    await ws.send(json.dumps(data))
    while True:
        try:
            data_rec = await asyncio.wait_for(ws.recv(), timeout=4)
            data_json: dict[str, str] = json.loads(data_rec)

            # if an `eos` value of `True` is received, break the loop.
            # this means the mentor has finished generating the response.
            if data_json.get("eos"):
                break

            # if `data` is present in the response,
            # then this is a token that needs to be shown to the user.
            data_to_write = data_json.get("data")
            if data_to_write:
                # print the token to the console.
                print(data_to_write, end="")

        except asyncio.TimeoutError:
            sys.stdout.write("\n")
            break
    await ws.close()


async def start():

    mentor_data = await create_mentor()
    if not mentor_data:
        return
    await upload_pdf_document_to_mentor(
        mentor_name=mentor_name,
        # replace with path to file
        file_path=Path("doc.pdf"),
    )

    await wait_for_document_training_to_complete(mentor_name)

    session_id = await create_chat_session(mentor_name)
    await chat_with_websocket(
        session_id=session_id,
        mentor=mentor_name,
        tenant=tenant,
        username=username,
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
