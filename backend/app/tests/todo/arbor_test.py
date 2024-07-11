import requests
import os
import sys
import json

# Define the base URL and the tokens
base_url = f"http://{os.environ.get('BACKEND_URL', 'localhost')}:{os.environ.get('BACKEND_PORT', '9500')}/arbor/data"
tokens = {
    1: os.getenv("KS3_COURSE_CLASS_MEMBERSHIP_AUTH"),
    2: os.getenv("TEACHING_GROUP_MEMBERSHIPS_2023_2024_AUTH"),
    3: os.getenv("SCHEDULED_TIMETABLE_SLOTS_AUTH"),
    4: os.getenv("BEHAVIOURAL_INCIDENTS_REPORTING_AUTH"),
    5: os.getenv("Y7_LESSON_TIMETABLE_AUTH")
}

def test_fetch_arbor_data(id, token):
    endpoint = f"{base_url}/{id}"
    headers = {"Authorization": f"Basic {token}"}
    params = {"token": token}
    
    response = requests.get(endpoint, headers=headers, params=params)
    
    if response.status_code == 200:
        print(json.dumps(response.json()))
    else:
        print(f"Failed for ID {id}:", response.status_code, response.text, file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python arbor_test.py <id>", file=sys.stderr)
        sys.exit(1)
    
    try:
        id = int(sys.argv[1])
    except ValueError:
        print("ID must be an integer", file=sys.stderr)
        sys.exit(1)
    
    token = tokens.get(id)
    if token:
        test_fetch_arbor_data(id, token)
    else:
        print(f"Token for ID {id} is not set", file=sys.stderr)