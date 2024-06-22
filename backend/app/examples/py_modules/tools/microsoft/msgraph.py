print("PRINT STATEMENT: Loading msgraph.py...")
import sys
import os
import requests

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
sys.path.append(os.getenv("PY_MODULES_PATH"))
import setup_dev as dev
env = dev.get_env()
import logger_tool as logger
logging = logger.get_logger(name='logger_tool')

def login():
    logging.pedantic("Logging in...")
    # Testing with client credentials flow
    username = None
    password = None
    if username is None and password is None:
        logging.info("No username or password provided. Using default client credentials flow...")
        url = f"{env.msgraph_authority_url}/{env.msgraph_tenant_id}/oauth2/v2.0/token" 
        payload = {
            "grant_type": "client_credentials",
            "client_id": env.msgraph_client_id,
            "client_secret": env.msgraph_client_secret,
            "scope": "https://graph.microsoft.com/.default"
        }
        logging.pedantic("Getting access token from " + url + " with payload: " + str(payload))
        response = requests.post(url, data=payload)
        logging.debug("Response: " + str(response))
        access_token = response.json().get('access_token')
        if access_token is None:
            logging.error("No access token found")
            return None
        else:
            logging.debug("Found access token: " + access_token)
            return access_token
    else:
        logging.error("An error has occured.")
        return None

def get_user_id(access_token=None):
    logging.pedantic("Getting user ID...")
    if access_token is None:
        logging.warning("No access token provided. Exiting...")
        return None
    logging.pedantic("Getting user ID with access token: " + access_token)
    url = f"{env.msgraph_resource_url}/{env.msgraph_api_version}/users"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    users = response.json().get('value', [])

    # For simplicity, this example just returns the ID of the first user.
    # In a real application, you'd want to search for a specific user,
    # or provide a mechanism for selecting a user from the returned list.
    if users:
        logging.info("Found user: " + users[0]['id'])
        return users[0]['id']  # or 'userPrincipalName'
    else:
        logging.warning("No users found.")
        return None

