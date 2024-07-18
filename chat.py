import asyncio
import json
import sys
from websockets.client import connect


# THIS ENDPOINT ALLOWS ALL USERS TO CHAT WITH MENTORS.
# ALSO NOTE THAT WHEN MENTOR IS SET TO ANONYMOUS EVEN ANONYMOUS USERS CAN CHAT

# Manager base url to be changed
ASGI_BASE_URL = "wss://asgi.data.<DOMAIN>"

# user details to be changed
TENANT = ""
USERNAME = ""
ACCESS_TOKEN = ""  # this must be a tenant api key

async def chat_with_mentor():
    """
    Chat with mentor.
    """
    
    mentor = "" # This can mentor slug or mentor unique id.
    data = {
        "flow": {"name": mentor, "tenant": TENANT, "username": USERNAME},
        "session_id": "", # session id generated forthis mentor and user.
        "token": ACCESS_TOKEN,
        "pathway": mentor,
        "prompt": "Who is Rayana Barnawi",
    }
    ws = await connect(f"{ASGI_BASE_URL}/ws/langflow/")
    await ws.send(json.dumps(data))
    received_data = await ws.recv()
    print(received_data)
    print("websocket status", json.loads(received_data)["detail"])
    print(f"Question: {data.get('prompt')}")
    await ws.send(json.dumps(data))
    while True:
        try:
            data_rec = await asyncio.wait_for(ws.recv(), timeout=4)
            data_json = json.loads(data_rec)
            data_to_write = data_json.get("data")
            if data_to_write:
                sys.stdout.write(data_to_write)
        except asyncio.TimeoutError:
            sys.stdout.write("\n")
            break


loop = asyncio.get_event_loop()
loop.run_until_complete(chat_with_mentor())
