#!/usr/bin/env python3
"""
Reply 'hey' to the latest edX discussion threads and/or create new discussion threads.

Prereqs:
- pip install requests python-dateutil

Configurable via environment variables:
- EDX_BASE_URL: LMS base URL (no trailing slash)
- EDX_OAUTH2_TOKEN: Bearer token for admin API access
- EDX_COURSE_ID: Optional course ID to scope threads
- MAX_THREADS_TO_REPLY: How many latest threads to reply to (default 20)
- ONLY_WITHIN_HOURS: Only threads active within last N hours (default 72)
- POST_SLEEP_SECONDS: Delay between posts to avoid hammering the API (default 0.25)
- CREATE_NEW_THREADS: Whether to create new discussion threads (default false)
- NEW_THREAD_TITLE: Title for new threads (default "Sample Discussion")
- NEW_THREAD_BODY: Body content for new threads (default "Sample discussion content")
- NEW_THREAD_TOPIC_ID: Topic ID for new threads (default "course")
- NEW_THREAD_TYPE: Type of new threads (default "discussion")
- NEW_THREAD_COUNT: Number of new threads to create (default 1)
"""

import os
import time
import json
import logging
from typing import Generator, Dict, Optional
from datetime import datetime, timezone
import requests
from dateutil import parser as dateparser
import asyncio
import api
import websockets
import sys


# ---------- Configuration ----------
EDX_BASE_URL = os.getenv("EDX_BASE_URL", "https://learn.iblai.org")
OAUTH2_TOKEN = os.getenv("EDX_OAUTH2_TOKEN", "jSyCAMrxoXWLTso0mmPgeSkkx5roCi")
COURSE_ID = os.getenv("EDX_COURSE_ID", "course-v1:main+NB2025+2025_T1")   # e.g. "course-v1:main+NB2025+2025_T1"
MAX_THREADS_TO_REPLY = int(os.getenv("MAX_THREADS_TO_REPLY", "20"))
ONLY_WITHIN_HOURS = int(os.getenv("ONLY_WITHIN_HOURS", "72"))
POST_SLEEP_SECONDS = float(os.getenv("POST_SLEEP_SECONDS", "0.25"))

# New thread creation configuration
CREATE_NEW_THREADS = os.getenv("CREATE_NEW_THREADS", "false").lower() == "true"
NEW_THREAD_TITLE = os.getenv("NEW_THREAD_TITLE", "Sample Discussion")
NEW_THREAD_BODY = os.getenv("NEW_THREAD_BODY", "Sample discussion content")
NEW_THREAD_TOPIC_ID = os.getenv("NEW_THREAD_TOPIC_ID", "course")
NEW_THREAD_TYPE = os.getenv("NEW_THREAD_TYPE", "discussion")
NEW_THREAD_COUNT = int(os.getenv("NEW_THREAD_COUNT", "1"))

# AI author configuration
AI_AUTHOR_NAME = os.getenv("AI_AUTHOR_NAME", "ibl_admin")

# Course metadata caching
_course_metadata = None


# Mentor configuration
TENANT = os.getenv("IBL_TENANT", "skillsai")
USERNAME = os.getenv("IBL_USERNAME", "gipsbrian")
PLATFORM_API_KEY = os.getenv("IBL_PLATFORM_API_KEY", "11fce3794bb72dbcc57c58e73b8ba9e36345c645dd87afea953ca19978452e54")
MENTOR_ID = os.getenv("IBL_MENTOR_ID", "mentorAI")
SESSION_ID = os.getenv("IBL_SESSION_ID")


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ---------- API Session ----------
SESSION = requests.Session()
SESSION.headers.update({
    "Authorization": f"Bearer {OAUTH2_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
})

# ---------- Helper Functions ----------
def list_threads(course_id: Optional[str] = None, page_size: int = 50) -> Generator[Dict, None, None]:
    """Yield discussion threads with pagination, most recent first."""
    url = f"{EDX_BASE_URL}/api/discussion/v1/threads/"
    params = {
        "page_size": page_size,
        "order_by": "last_activity_at",
        "order_direction": "desc",
    }
    if course_id:
        params["course_id"] = course_id

    while True:
        # Build full URL for logging
        full_url = f"{url}?" + "&".join([f"{k}={v}" for k, v in params.items()])
        logging.info(f"GET {full_url}")
        logging.debug(f"GET {url} params={params}")
        resp = SESSION.get(url, params=params, timeout=30)
        logging.info(f"Response: {resp.status_code}")
        if resp.status_code != 200:
            raise RuntimeError(f"Failed to list threads: {resp.status_code} {resp.text}")
        data = resp.json()

        # Log the response summary
        logging.info("=== GET Threads Response ===")
        logging.info(f"Found {len(data.get('results', []))} threads")

        results = data.get("results", [])
        for thread in results:
            yield thread
        next_url = data.get("next")
        if not next_url:
            break
        logging.info(f"Pagination: GET {next_url}")
        url = next_url
        params = {}

def post_comment(thread_id: str, body: str) -> Dict:
    """Post a top-level comment to a thread."""
    url = f"{EDX_BASE_URL}/api/discussion/v1/comments/"
    payload = {
        "thread_id": thread_id,
        "raw_body": body,
    }
    logging.info(f"POST {url}")
    logging.info("=== POST Comment Payload ===")
    logging.info(f"Thread ID: {thread_id}, Body length: {len(body)} chars")
    logging.debug(f"POST {url} json={payload}")
    resp = SESSION.post(url, data=json.dumps(payload), timeout=30)
    logging.info(f"Response: {resp.status_code}")

    # Log the response from POST comment
    if resp.status_code in (200, 201):
        response_data = resp.json()
        logging.info("=== POST Comment Response ===")
        logging.info(f"Comment ID: {response_data.get('id', 'N/A')}, Author: {response_data.get('author', 'N/A')}")
    else:
        logging.error(f"Failed to post comment to thread {thread_id}: {resp.status_code} {resp.text}")
        raise RuntimeError(f"Failed to post comment to thread {thread_id}: {resp.status_code} {resp.text}")

    return resp.json()

def is_within_hours(ts: str, hours: Optional[int]) -> bool:
    if hours is None:
        return True
    try:
        dt = dateparser.parse(ts)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - dt.astimezone(timezone.utc)
        return delta.total_seconds() <= hours * 3600
    except Exception:
        return True  # fail-open

def get_course_metadata(course_id: str) -> dict:
    """Fetch course metadata to provide context for AI mentor."""
    global _course_metadata

    # Return cached metadata if available
    if _course_metadata is not None:
        return _course_metadata

    try:
        # Extract course key from course_id if needed
        course_key = course_id
        if not course_key.startswith("course-v1:"):
            course_key = f"course-v1:{course_id}"

        url = f"{EDX_BASE_URL}/api/ibl/v1/course_metadata"
        params = {"course_key": course_key}

        logging.info(f"Fetching course metadata for: {course_key}")
        logging.info(f"GET {url} params={params}")

        resp = SESSION.get(url, params=params, timeout=30)
        logging.info(f"Response: {resp.status_code}")

        if resp.status_code != 200:
            logging.warning(f"Failed to get course metadata: {resp.status_code}")
            return {}

        metadata = resp.json()

        # Log the course metadata
        logging.info("=== Course Metadata Response ===")
        logging.info(f"Course: {metadata.get('display_name', 'Unknown')} - {metadata.get('org', 'N/A')}")

        # Cache the metadata
        _course_metadata = metadata

        return metadata

    except Exception as e:
        logging.error(f"Error fetching course metadata: {str(e)}")
        return {}

def has_ai_already_replied(thread_id: str) -> bool:
    """Check if the AI has already replied to this thread by looking at the latest comment."""
    try:
        url = f"{EDX_BASE_URL}/api/discussion/v1/comments/"
        params = {
            "thread_id": thread_id,
            "page": 1,
            "reverse_order": "true",
            "requested_fields": "profile_image",
            "enable_in_context_sidebar": "false"
        }

        logging.info(f"Checking comments for thread {thread_id}")
        logging.info(f"GET {url} params={params}")

        resp = SESSION.get(url, params=params, timeout=30)
        logging.info(f"Response: {resp.status_code}")

        if resp.status_code != 200:
            logging.warning(f"Failed to get comments for thread {thread_id}: {resp.status_code}")
            return False  # If we can't check, assume we haven't replied

        data = resp.json()
        comments = data.get("results", [])

        # Log the comments response
        logging.info("=== Thread Comments Response ===")
        logging.info(f"Found {len(comments)} comments")

        if not comments:
            logging.info(f"No comments found for thread {thread_id}")
            return False

        # Get the latest comment (first in reverse order)
        latest_comment = comments[0]
        latest_author = latest_comment.get("author", "")

        logging.info(f"Latest comment author: {latest_author}")
        logging.info(f"AI author name: {AI_AUTHOR_NAME}")

        # Check if the latest comment is from our AI author
        has_replied = latest_author == AI_AUTHOR_NAME

        if has_replied:
            logging.info(f"AI has already replied to thread {thread_id} (latest author: {latest_author})")
        else:
            logging.info(f"AI has not replied to thread {thread_id} (latest author: {latest_author})")

        return has_replied

    except Exception as e:
        logging.error(f"Error checking if AI has replied to thread {thread_id}: {str(e)}")
        return False  # If we can't check, assume we haven't replied

async def capture_ai_response(prompt: str, session_id: str, mentor: str, tenant: str, username: str, api_key: str) -> str:
    """Capture AI response from websocket and return the content."""
    try:
        # Use the same websocket approach as the API but capture the response
        ws_url = f"{api.ASGI_URL}/ws/chat/{session_id}"
        headers = {"Authorization": f"Bearer {api_key}"}

        async with websockets.connect(ws_url, extra_headers=headers) as ws:
            # Send the prompt
            await ws.send(json.dumps({"prompt": prompt}))

            # Collect the response
            response_parts = []
            eos = False

            while not eos:
                try:
                    data = await asyncio.wait_for(ws.recv(), timeout=30)
                    msg = json.loads(data)

                    if "error" in msg:
                        logging.error(f"Error from server: {msg['error']}")
                        return f"Error: {msg['error']}"

                    if "data" in msg:
                        response_parts.append(msg["data"])
                        logging.info(f"Received AI token: {msg['data']}")

                    if msg.get("eos"):
                        eos = True
                        logging.info("AI response completed (EOS received)")

                except asyncio.TimeoutError:
                    logging.warning("Timeout while waiting for response")
                    break

            # Join all response parts
            full_response = "".join(response_parts)
            logging.info(f"Captured Full AI Response: {full_response}")
            return full_response

    except Exception as e:
        logging.error(f"Error capturing AI response: {str(e)}")
        return f"Thank you for sharing this discussion. I appreciate your contribution to our community dialogue."

# Global session for reuse across all AI requests
_ai_session_id = None

async def generate_llm_response_for_discussion(thread_data: dict) -> dict:
    """
    Given a discussion thread's data, use the API to generate a response payload.

    Args:
        thread_data (dict): Full thread data from the API

    Returns:
        dict: The LLM-generated response object (payload) as returned by the API
    """
    global _ai_session_id

    logging.info("=== AI Response Generation Started ===")

    # Extract thread information
    title = thread_data.get("title", "")
    body = thread_data.get("raw_body", "")
    author = thread_data.get("author", "")
    created_at = thread_data.get("created_at", "")
    comment_count = thread_data.get("comment_count", 0)

    logging.info(f"Thread Title: {title}")
    logging.info(f"Thread Author: {author}")
    logging.info(f"Thread Created: {created_at}")
    logging.info(f"Comment Count: {comment_count}")
    logging.info(f"Thread Body: {body}")

    # Get course metadata for better context
    course_metadata = get_course_metadata(COURSE_ID)

    # Extract relevant course information
    course_title = course_metadata.get("display_name", "Unknown Course")
    course_overview = course_metadata.get("overview", "")
    course_description = course_metadata.get("description", "")
    course_short_desc = course_metadata.get("short_description", "")

    # Clean up HTML from overview for better AI processing
    import re
    if course_overview:
        # Remove HTML tags but keep content
        course_overview = re.sub(r'<[^>]+>', ' ', course_overview)
        course_overview = re.sub(r'\s+', ' ', course_overview).strip()

    # Create comprehensive context for the AI
    discussion_prompt = f"""Course Context:
Course Title: {course_title}
Course Description: {course_description or course_short_desc}
Course Overview: {course_overview[:500] if course_overview else "No overview available"}

Discussion Thread Context:
Title: {title}
Author: {author}
Created: {created_at}
Existing Comments: {comment_count}
Content: {body}

As a mentor for this course, please provide a thoughtful and helpful response to this discussion thread. Use your knowledge of the course content and context to provide relevant guidance."""

    logging.info(f"Combined Prompt: {discussion_prompt}")

    # Log the data being sent to LLM
    logging.info("=== Data Sent to LLM ===")
    logging.info(f"Thread: {title} by {author}")
    logging.info(f"Prompt length: {len(discussion_prompt)} chars")

    # Reuse existing session or create new one
    session_id = _ai_session_id or SESSION_ID
    mentor_unique_id = MENTOR_ID

    if not session_id:
        logging.info("Creating new session for mentor...")
        session_id = api.create_chat_session(
            username=USERNAME,
            tenant=TENANT,
            mentor_unique_id=mentor_unique_id,
        )
        _ai_session_id = session_id  # Store for reuse
        logging.info(f"Created Session ID: {session_id}")
    else:
        logging.info(f"Reusing existing Session ID: {session_id}")

    logging.info("Calling API with parameters:")
    logging.info(f"  Session ID: {session_id}")
    logging.info(f"  Mentor ID: {mentor_unique_id}")
    logging.info(f"  Tenant: {TENANT}")
    logging.info(f"  Username: {USERNAME}")
    logging.info(f"  API Key: {PLATFORM_API_KEY[:10]}...")

    # Use the API to chat with mentor (following quickstart pattern exactly)
    logging.info("Sending request to AI mentor...")

    # Capture the AI response properly
    try:
        ai_content = await capture_ai_response(
            prompt=discussion_prompt,
            session_id=session_id,
            mentor=mentor_unique_id,
            tenant=TENANT,
            username=USERNAME,
            api_key=PLATFORM_API_KEY,
        )

    except Exception as e:
        logging.error(f"Error with AI mentor: {str(e)}")
        ai_content = f"Thank you for sharing this discussion. I appreciate your contribution to our community dialogue."

    logging.info("=== AI Response Generation Completed ===")
    logging.info(f"AI Generated Content: {ai_content}")

    # Return a structured response with the AI content
    return {
        "content": ai_content,
        "body": ai_content,
        "message": ai_content
    }



async def create_thread(course_id: str, title: str, body: str, topic_id: str = "course", thread_type: str = "discussion") -> Dict:
    """Create a new discussion thread."""
    url = f"{EDX_BASE_URL}/api/discussion/v1/threads/"

    # Generate AI response
    logging.info("Generating AI response for discussion...")
    # Create a mock thread data for AI generation
    mock_thread_data = {
        "title": title,
        "raw_body": body,
        "author": "System",
        "created_at": datetime.now().isoformat(),
        "comment_count": 0
    }
    response = await generate_llm_response_for_discussion(mock_thread_data)
    logging.info(f"AI Response: {json.dumps(response, indent=2)}")

    # Extract AI-generated content from response - keep original title, use AI for body
    ai_title = title  # Keep original title as requested
    ai_body = response.get("body", response.get("content", body))  # Use AI body/content or fallback to original

    logging.info(f"Using Original Title: {ai_title}")
    logging.info(f"AI Generated Body: {ai_body}")

    payload = {
        "course_id": course_id,
        "topic_id": topic_id,
        "type": thread_type,
        "title": ai_title,
        "raw_body": ai_body,
        "following": True,
        "anonymous": False,
        "enable_in_context_sidebar": False
    }
    logging.info(f"POST {url}")
    logging.info("=== POST Thread Payload ===")
    logging.info(f"Title: {title}, Body length: {len(body)} chars, Topic: {topic_id}")
    logging.debug(f"POST {url} json={payload}")
    resp = SESSION.post(url, data=json.dumps(payload), timeout=30)
    logging.info(f"Response: {resp.status_code}")

    # Log the response from POST thread
    if resp.status_code in (200, 201):
        response_data = resp.json()
        logging.info("=== POST Thread Response ===")
        logging.info(f"Thread ID: {response_data.get('id', 'N/A')}, Author: {response_data.get('author', 'N/A')}")
    else:
        logging.error(f"Failed to create thread: {resp.status_code} {resp.text}")
        raise RuntimeError(f"Failed to create thread: {resp.status_code} {resp.text}")

    return resp.json()

# ---------- Main Logic ----------
async def main():
    if not OAUTH2_TOKEN or OAUTH2_TOKEN.startswith("<"):
        raise SystemExit("Please set EDX_OAUTH2_TOKEN to a valid OAuth2 bearer token.")

    if not COURSE_ID:
        raise SystemExit("Please set EDX_COURSE_ID to a valid course ID.")

    total_replied = 0
    total_created = 0

    # Create new threads if requested
    if CREATE_NEW_THREADS:
        logging.info(f"Creating {NEW_THREAD_COUNT} new discussion threads...")
        for i in range(NEW_THREAD_COUNT):
            try:
                # Add a timestamp to make titles unique
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                title = f"{NEW_THREAD_TITLE} - {timestamp}"
                body = f"{NEW_THREAD_BODY} - Created at {timestamp}"

                result = await create_thread(
                    course_id=COURSE_ID,
                    title=title,
                    body=body,
                    topic_id=NEW_THREAD_TOPIC_ID,
                    thread_type=NEW_THREAD_TYPE
                )
                total_created += 1
                thread_id = result.get("id", "unknown")
                logging.info(f"Created new thread: {title} (ID: {thread_id})")
            except Exception as e:
                logging.error(f"Failed to create thread: {str(e)}")

            time.sleep(POST_SLEEP_SECONDS)

    # Reply to existing threads if configured
    if MAX_THREADS_TO_REPLY > 0:
        logging.info("Fetching latest discussion threads to reply to...")
        replied = 0
        checked = 0

        for thread in list_threads(course_id=COURSE_ID):
            checked += 1
            thread_id = thread.get("id") or thread.get("thread_id")
            title = thread.get("title", "")
            last_activity_at = thread.get("last_activity_at") or thread.get("updated_at") or thread.get("created_at")
            closed = thread.get("closed", False)

            if ONLY_WITHIN_HOURS and last_activity_at and not is_within_hours(last_activity_at, ONLY_WITHIN_HOURS):
                continue
            if closed or not thread_id:
                logging.info(f"Skipping thread: {title} ({thread_id})")
                continue

            # Check if AI has already replied to this thread
            if has_ai_already_replied(thread_id):
                logging.info(f"Skipping thread {title} ({thread_id}) - AI has already replied")
                continue

            try:
                # Generate AI response for the thread using full thread data
                logging.info(f"Generating AI response for thread: {title}")
                ai_response = await generate_llm_response_for_discussion(thread)

                # Extract AI-generated content for the reply
                ai_reply = ai_response.get("body", ai_response.get("content", "Thank you for sharing this discussion!"))
                logging.info(f"AI Generated Reply: {ai_reply}")

                _ = post_comment(thread_id, ai_reply)
                replied += 1
                logging.info(f"Replied with AI response to thread: {title} ({thread_id})")
            except Exception as e:
                logging.error(f"Failed to generate AI response for thread {title}: {str(e)}")
                # Fallback to simple reply if AI fails
                try:
                    _ = post_comment(thread_id, "Thank you for sharing this discussion!")
                    replied += 1
                    logging.info(f"Replied with fallback message to thread: {title} ({thread_id})")
                except Exception as fallback_error:
                    logging.error(f"Failed to post fallback reply: {str(fallback_error)}")

            time.sleep(POST_SLEEP_SECONDS)
            if MAX_THREADS_TO_REPLY and replied >= MAX_THREADS_TO_REPLY:
                break

        total_replied = replied
        logging.info(f"Checked threads: {checked}")
        logging.info(f"Replied to threads: {total_replied}")

    # Summary
    logging.info(f"Summary:")
    logging.info(f"  Created new threads: {total_created}")
    logging.info(f"  Replied to existing threads: {total_replied}")
    logging.info(f"  Total operations: {total_created + total_replied}")

if __name__ == "__main__":
    asyncio.run(main())
