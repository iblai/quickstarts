# quickstarts
## Installation
- Create a new virtual environment and activate it
- Install the requirements in `requirements/base.txt`

```shell
# uv
uv venv
source .venv/bin/activate
uv pip install -r requirements/base.txt

# pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/base.txt
```

## Quickstart
The `quickstart.py` file allows you to create a mentor, a session, and then chat with it.

Set the following environment variables (required):
```shell
export IBL_TENANT=<your tenant>
export IBL_USERNAME=<your username>
export IBL_PLATFORM_API_KEY=<your platform API key>
```

You may optionally set the following environment variables:
```shell
# Set IBL_MENTOR_ID to create a new chat session with an existing mentor
export IBL_MENTOR_ID=<mentor id> 

# Set IBL_SESSION_ID to continue chatting using a previous session instead of creating a new one
# IBL_MENTOR_ID must be set to the same mentor id associated with this session
export IBL_SESSION_ID=<session id>
```

To run the quickstart file:
- Ensure you virtual environment is activated
- Run:

```shell
python quickstart.py "Your prompt here"
```
