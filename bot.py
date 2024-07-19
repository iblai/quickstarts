from typing import Literal, Optional
import requests

TENANT = ""
USERNAME = ""
ACCESS_TOKEN = ""  # this must be a TENANT api key

MANAGER_URL = (
    "https://base.manager.iblai.app"  # updating to the corresponding data manager url.
)


def create_bot(
    name,
    client_id: str,
    secret_key: str,
    app_token: str,
    verification_token: str,
    provider: Literal[
        "slack",
        "webex",
        "whatsapp",
        "discord",
    ],
    config: dict,
):
    """
    Create a bot with the provided parameters.

    Parameters:
        name: The name of the bot.
        client_id (str): The client ID of the bot.
        secret_key (str): The client secret of the bot.
        app_token (str): The app token of the bot.
        verification_token (str): The verification token of the bot.
        provider: Literal["slack", "webex", "whatsapp", "discord"]: The provider of the bot.
        config (dict): Configuration settings for the bot.

    Returns:
        dict or None: The JSON response of the bot if the bot is successfully created, None otherwise.
    """

    print("Creating or updating role...")
    url = f"{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot/"
    print(url)

    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "TENANT": TENANT,
        "name": name,
        "client_id": client_id,
        "client_secret": secret_key,
        "app_token": app_token,
        "verification_token": verification_token,
        "provider": provider,
        "config": config,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("Bot created successfully.")
        return response.json()
    else:
        print(
            f"Failed to create bot. Status code: {response.status_code}, Response: {response.text}"
        )
        return None


def update_bot(
    bot_id: int,
    name: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    app_token: Optional[str] = None,
    verification_token: Optional[str] = None,
    config: Optional[dict] = None,
) -> dict[None]:
    """
    Update a bot with the provided parameters.

    Parameters:
        bot_id (int): The ID of the bot to update.
        name (Optional[str], optional): The name of the bot. Defaults to None.
        client_id (Optional[str], optional): The client ID of the bot. Defaults to None.
        client_secret (Optional[str], optional): The client secret of the bot. Defaults to None.
        app_token (Optional[str], optional): The app token of the bot. Defaults to None.
        verification_token (Optional[str], optional): The verification token of the bot. Defaults to None.
        config (Optional[dict], optional): Configuration settings for the bot. Defaults to None.

    Returns:
        dict or None: The JSON response if the bot is successfully updated, None otherwise.
    """

    print("Creating or updating role...")
    url = f"{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot/{bot_id}/"
    print(url)

    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {}
    if name is not None:
        payload["name"] = name
    if client_id is not None:
        payload["client_id"] = client_id
    if client_secret is not None:
        payload["client_secret"] = client_secret
    if app_token is not None:
        payload["app_token"] = app_token
    if verification_token is not None:
        payload["verification_token"] = verification_token
    if config is not None:
        payload["config"] = config

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Bot Updated successfully.")
        return response.json()
    else:
        print(
            f"Failed to Update bot. Status code: {response.status_code}, Response: {response.text}"
        )
        return None


def create_bot_command(
    command: str,
    mentor_id: int,
    bot_id: int,
) -> dict | None:
    """
    Create a bot command.

    Parameters:
        command (str): The command to be associated with the bot.
        mentor_id (int): The ID of the mentor associated with the command.
        bot_id (int): The ID of the bot for which the command is created.

    Returns:
        dict or None: The JSON response of the created or updated bot command if successful, None otherwise.
    """
    print("Creating or updating bot command...")
    url = f"{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot-commands/"
    print(url)

    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "command": command,
        "mentor": mentor_id,
        "bot": bot_id,
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("Bot command created successfully.")
        return response.json()
    else:
        print(
            f"Failed to create bot command. Status code: {response.status_code}, Response: {response.text}"
        )
        return None


def update_bot_command(
    command_id: int,
    command: Optional[str] = None,
    mentor_id: Optional[int] = None,
    bot_id: Optional[int] = None,
) -> dict | None:
    """
    Update a bot command with the given parameters.

    Args:
        command_id (int): The ID of the bot command to update.
        command (Optional[str], optional): The new command to associate with the bot command. Defaults to None.
        mentor_id (Optional[int], optional): The new mentor ID to associate with the bot command. Defaults to None.
        bot_id (Optional[int], optional): The new bot ID to associate with the bot command. Defaults to None.

    Returns:
        dict or None: The JSON response of the updated bot command if successful, None otherwise.
    """
    print("Updating bot command...")
    url = f"{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot-commands/{command_id}"
    print(url)
    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {}
    if command is not None:
        payload["command"] = command
    if mentor_id is not None:
        payload["mentor"] = mentor_id
    if bot_id is not None:
        payload["bot"] = bot_id
    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Bot Command updated successfully.")
        return response.json()
    else:
        print(
            f"Failed to update bot command. Status code: {response.status_code}, Response: {response.text}"
        )
        return None


def delete_bot(bot_id: int) -> bool:
    """
    A function to delete a bot based on the provided bot_id.

    Parameters:
        bot_id (int): The ID of the bot to be deleted.

    Returns:
        bool: True if the bot is deleted successfully, False otherwise.
    """
    print("deleting bot command...")
    url = f"{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot/{bot_id}"
    print(url)

    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print("Bot deleted successfully")
        return True
    else:
        print(
            f"Failed to delete bot. Status code: {response.status_code}, Response: {response.text}"
        )
        return False


def delete_botcommand(command_id: int) -> bool:
    """
    A function to delete a bot command based on the provided command_id.

    Parameters:
        command_id (int): The ID of the command to be deleted.

    Returns:
        bool: True if the command is deleted successfully, False otherwise.
    """
    print("deleting bot command...")
    url = f"{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot-commands/{command_id}"
    print(url)

    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print("BotCommand deleted successfully")
        return True
    else:
        print(
            f"Failed to delete botcommand. Status code: {response.status_code}, Response: {response.text}"
        )
        return False


def list_bots() -> dict | None:
    """
    Retrieves a list of bots from the API.

    Returns:
        dict | None: A dictionary representing the list of bots if the request is successful, None otherwise.
    """
    url = f"{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot/"
    print(url)

    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Successfully retrieved list of bots successfully")
        return response.json()

    print("Failed to retrieve list of bots")
    return None


def list_bot_commands(bot_id: Optional[int] = None) -> dict | None:
    """
    Retrieves a list of bot commands from the API.

    Args:
        bot_id (Optional[int]): The ID of the bot for which to retrieve the commands. If not provided, commands for all bots will be returned.

    Returns:
        dict | None: A dictionary representing the list of bot commands if the request is successful, None otherwise.
    """
    url = f"{MANAGER_URL}/api/ai-bot/v1/bots/{TENANT}/bot-commands/"
    if bot_id:
        url = f"{url}?bot={bot_id}"

    headers = {
        "Authorization": f"Api-Token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Sucessfully retrieved list of bot ommands")
        return response.json()

    print("Failed to retrieve list of botcommands")
    return None

# update this data accordingly
BOT_DATA = {
    "name": "Test Bot",
    "client_id": "test-bot-client-id",
    "client_secret": "test-bot-client-secret",
    "app_token": "test-bot-app-token",
    "verification_token": "test-bot-verification-token",
    "config": {},
}

COMMAND_DATA = {
    "command": "/test-command",
    "mentor": 1,
}

if __name__ == "__main__":
    bot_id = None
    command_id = None
    bot_response = create_bot(**BOT_DATA)

    if bot_response:
        bot_id = bot_response["id"]
    command_response = create_bot_command(**COMMAND_DATA, bot_id=bot_id)

    if command_response:
        command_id = command_response["id"]
        delete_botcommand(command_id)
    if bot_id:
        delete_bot(bot_id)
