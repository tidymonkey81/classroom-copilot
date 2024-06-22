import sys
import os
import requests
import time
import json

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
sys.path.append(os.getenv("PY_MODULES_PATH"))
import setup_dev as dev
env = dev.get_env()
import logger_tool as logger
logging = logger.get_logger(name='logger_tool')

env = dev.get_env()

# Get OneNote Notebooks
def get_onenote_notebooks(access_token=None, user_id=None):
    if access_token is None or user_id is None:
        logging.error("No access token or user ID provided. Exiting...")
        logging.debug("Access token: " + str(access_token))
        logging.debug("User ID: " + str(user_id))
        return None
    url = f"{env.msgraph_resource_url}/{env.msgraph_api_version}/users/{user_id}/onenote/notebooks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    logging.pedantic("Getting notebooks from: " + url + " with headers: " + str(headers))
    response = requests.get(url, headers=headers)
    logging.pedantic("Response: " + str(response))
    notebooks = response.json().get('value', [])
    logging.info("Found notebooks: " + str(notebooks))
    return notebooks

# Get OneNote Sections
def get_onenote_sections(access_token=None, user_id=None, notebook_id=None):
    if access_token is None or user_id is None or notebook_id is None:
        logging.error("No access token, user ID, or notebook ID provided. Exiting...")
        logging.debug("Access token: " + str(access_token))
        logging.debug("User ID: " + str(user_id))
        logging.debug("Notebook ID: " + str(notebook_id))
        return None
    url = f"{env.msgraph_resource_url}/{env.msgraph_api_version}/users/{user_id}/onenote/notebooks/{notebook_id}/sections"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    logging.pedantic("Getting sections from: " + url + " with headers: " + str(headers))
    response = requests.get(url, headers=headers)
    logging.pedantic("Response: " + str(response))
    sections = response.json().get('value', [])
    logging.info("Found sections: " + str(sections))
    return sections

# Get OneNote Pages
def get_onenote_pages(access_token=None, user_id=None, notebook_id=None, section_id=None):
    if access_token is None or user_id is None or notebook_id is None or section_id is None:
        logging.error("No access token, user ID, notebook ID, or section ID provided. Exiting...")
        logging.debug("Access token: " + str(access_token))
        logging.debug("User ID: " + str(user_id))
        logging.debug("Notebook ID: " + str(notebook_id))
        logging.debug("Section ID: " + str(section_id))
        return None
    url = f"{env.msgraph_resource_url}/{env.msgraph_api_version}/users/{user_id}/onenote/pages"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    logging.pedantic("Getting pages from: " + url + " with headers: " + str(headers))
    response = requests.get(url, headers=headers)
    logging.pedantic("Response: " + str(response))
    pages = response.json().get('value', [])
    logging.info("Found pages: " + str(pages))
    return pages

# Create OneNote Page
def create_onenote_page(access_token=None, user_id=None, section_id=None, title=None, content=None):
    if access_token is None or user_id is None or section_id is None or title is None or content is None:
        logging.error("No access token, user ID, section ID, title, or content provided. Exiting...")
        logging.debug("Access token: " + str(access_token))
        logging.debug("User ID: " + str(user_id))
        logging.debug("Section ID: " + str(section_id))
        logging.debug("Title: " + str(title))
        logging.debug("Content: " + str(content))
        return None
    url = f"{env.msgraph_resource_url}/{env.msgraph_api_version}/users/{user_id}/onenote/sections/{section_id}/pages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/xhtml+xml"
    }
    logging.pedantic("Creating page at: " + url + " with headers: " + str(headers))
    # The payload should include today's date in the <meta> tag
    created_date = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    logging.pedantic("Created date: " + created_date)
    payload = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    <meta name="created" content="{created_date}" />
    </head>
    <body>
    <p>{content}</p>
    </body>
    </html>
    """
    logging.pedantic("Payload: " + payload)
    response = requests.post(url, headers=headers, data=payload)
    logging.pedantic("Response: " + str(response))
    page = response.json()
    logging.info("Created page: " + str(page))
    return page

# Get OneNote Page Content
def get_onenote_page_content(access_token=None, user_id=None, page_id=None):
    if access_token is None or user_id is None or page_id is None:
        logging.error("No access token, user ID, or page ID provided. Exiting...")
        logging.debug("Access token: " + str(access_token))
        logging.debug("User ID: " + str(user_id))
        logging.debug("Page ID: " + str(page_id))
        return None
    url = f"{env.msgraph_resource_url}/{env.msgraph_api_version}/users/{user_id}/onenote/pages/{page_id}/content"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    logging.pedantic("Getting page content from: " + url + " with headers: " + str(headers))
    response = requests.get(url, headers=headers)
    logging.pedantic("Response: " + str(response))    
    # Check if the response is OK
    if response.status_code == 200:
        logging.pedantic("Found page content: " + str(response.text))
        content = response.text
    else:
        # If there's an error, it's likely in JSON format
        logging.error("Error getting page content: " + str(response))
        logging.debug("Error message: " + str(response.json()))
        content = None
    logging.info("Content: " + content)
    return content

# Append OneNote Page Content
def append_onenote_page_content(access_token=None, user_id=None, page_id=None, content=None):
    if access_token is None or user_id is None or page_id is None or content is None:
        logging.error("No access token, user ID, page ID, or content provided. Exiting...")
        logging.debug("Access token: " + str(access_token))
        logging.debug("User ID: " + str(user_id))
        logging.debug("Page ID: " + str(page_id))
        logging.debug("Content: " + str(content))
        return None
    url = f"{env.msgraph_resource_url}/{env.msgraph_api_version}/users/{user_id}/onenote/pages/{page_id}/content"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    logging.pedantic("Appending page content at: " + url + " with headers: " + str(headers))
    # Payload to append new content to the page
    data = [
        {
            "target": "body",
            "action": "append",  # Use 'replace' to replace entire content
            "content": f"<p>{content}</p>"
        }
    ]
    logging.pedantic("Data: " + str(data))
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    logging.pedantic("Response: " + str(response))
    if response.status_code == 204:
        logging.info("Page content appended successfully.")
        return None
    else:
        logging.error("Error appending page content: " + response.json())
        return None

# Move OneNote Page
def move_onenote_page(access_token=None, user_id=None, page_id=None, section_id=None):
    if access_token is None or user_id is None or page_id is None or section_id is None:
        logging.error("No access token, user ID, page ID, or section ID provided. Exiting...")
        logging.debug("Access token: " + str(access_token))
        logging.debug("User ID: " + str(user_id))
        logging.debug("Page ID: " + str(page_id))
        logging.debug("Section ID: " + str(section_id))
        return None
    url = f"{env.msgraph_resource_url}/{env.msgraph_api_version}/users/{user_id}/onenote/pages/{page_id}/copyToSection"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    logging.pedantic("Moving page at: " + url + " with headers: " + str(headers))
    payload = {
        "id": section_id  # ID of the destination section
    }
    logging.pedantic("Payload: " + str(payload))
    response = requests.post(url, headers=headers, json=payload)
    logging.pedantic("Response: " + str(response))
    time.sleep(5)  # Wait for a second
    url = f"{env.msgraph_resource_url}/{env.msgraph_api_version}/users/{user_id}/onenote/pages/{page_id}"
    logging.pedantic("Deleting page at: " + url + " with headers: " + str(headers))
    response = requests.delete(url, headers=headers)
    logging.pedantic("Response: " + str(response))
    if response.status_code == 204:
        logging.info("Page moved successfully.")
        return None
    else:
        logging.error("Error moving page: " + response.json())
        return None
    