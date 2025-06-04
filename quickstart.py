from __future__ import annotations

import asyncio
import json
import logging
import random
import sys
import typing as t

import requests
from websockets.client import connect

logging.basicConfig(level=logging.INFO, format="%(message)s")

log = logging.getLogger(__name__)

MANAGER_URL = "https://base.manager.iblai.tech/"
ASGI_URL = "wss://asgi.data.iblai.tech"
TENANT = ""  # platform key of tenant. eg: main
USERNAME = ""  # platform admin username
PLATFORM_API_KEY = ""


def create_mentor(api_token: str, settings: dict[str, str]) -> dict[str, t.Any]:
    """Create a new mentor with the provided settings."""
    headers = {"Authorization": f"Token {api_token}"}
    resp = requests.post(
        f"{MANAGER_URL}api/ai-mentor/orgs/{TENANT}/users/{USERNAME}/mentor-with-settings/",
        headers=headers,
        json=settings,
    )
    if not resp.ok:
        log.error(
            "Failed to create mentor (status=%s): %s",
            resp.status_code,
            resp.json(),
        )
        sys.exit(1)
    return resp.json()


def create_chat_session(username: str, mentor_unique_id: str) -> str:
    """Create a new chat session for the given user and mentor."""
    resp = requests.post(
        f"{MANAGER_URL}api/ai-mentor/orgs/{TENANT}/users/{username}/sessions/",
        json={"mentor": mentor_unique_id},
    )
    if not resp.ok:
        log.error(
            "Failed to create chat session (status=%s): %s",
            resp.status_code,
            resp.json(),
        )
        sys.exit(1)
    session_id = resp.json().get("session_id")
    return session_id


async def chat_with_websocket(
    prompt: str, session_id: str, mentor: str, tenant: str, username: str
):
    data = {
        "flow": {
            "name": mentor,
            "tenant": tenant,
            "username": username,
            "pathway": mentor,
        },
        "session_id": session_id,
        "token": PLATFORM_API_KEY,
        "prompt": prompt,
    }

    ws = await connect(f"{ASGI_URL}/ws/langflow/")
    log.info("Connected to Mentor")
    print("Response: ", end="")
    await ws.send(json.dumps(data))
    eos = False
    while not eos:
        try:
            data = await asyncio.wait_for(ws.recv(), timeout=10)
            msg: dict[str, str] = json.loads(data)
            if "error" in msg:
                log.error("Error from server: %s", msg["error"])
                await ws.close()
                sys.exit(1)

            if "data" in msg:
                print(msg["data"], end="", flush=True)

            if msg.get("eos"):
                eos = True
                print("")

        except asyncio.TimeoutError:
            log.warning("Timeout while waiting for response. Exiting...")
            await ws.close()
            sys.exit(1)

    await ws.close()


def run(prompt: str, mentor_unique_id: str = "", session_id: str = "") -> None:
    """Chat with a mentor using an existing mentor/session or create a new one.

    - Provide a mentor_unique_id to create a new session with an existing mentor.
    - Provide a mentor_unique_id and session_id to continue an existing session.
    """
    if not mentor_unique_id:
        mentor_name = f"Mentor-{random.randint(0, 100)}"
        log.info("Creating a new mentor: %s", mentor_name)
        mentor_settings = {
            "new_mentor_name": mentor_name,
            "template_name": "ai-mentor",
            "display_name": mentor_name,
            "description": "A mentor used to explain difficult concepts in simple terms",
            "system_prompt": "Explain it like the user is a 5-year-old",
        }
        mentor = create_mentor(api_token=PLATFORM_API_KEY, settings=mentor_settings)
        mentor_unique_id = mentor["unique_id"]
        log.info("Created Mentor: %s", mentor_unique_id)
    else:
        log.info("Using existing Mentor: %s", mentor_unique_id)

    if not session_id:
        session_id = create_chat_session(
            username=USERNAME, mentor_unique_id=mentor_unique_id
        )
        log.info("Created Session ID: %s", session_id)
    else:
        log.info("Using existing Session ID: %s", session_id)

    asyncio.run(
        chat_with_websocket(
            prompt=prompt,
            session_id=session_id,
            mentor=mentor_unique_id,
            tenant=TENANT,
            username=USERNAME,
        )
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        log.error('Usage: python quickstart.py "<prompt>"')
        sys.exit(1)
    prompt = sys.argv[1]
    run(
        prompt,
        mentor_unique_id="",
        session_id="",
    )
