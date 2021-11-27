import random
import requests
import populate

users, msgs = populate.get_data()

URL = "http://127.0.0.1:80"


def check_status_code(resp: requests.Response, expected: int):
    """Check the status code matches the expectation."""
    if resp.status_code != expected:
        raise ValueError("ERROR: response status code was {}, expected {}"
                         .format(resp.status_code, expected))


def check_app_json(resp: requests.Response):
    """Check the response is an 'application/json' from header."""
    if 'application/json' not in resp.headers['content-type']:
        raise ValueError("ERROR: expected 'application/json' in header, not"
                         "found. Did you jsonify your response?")


def check_length(list1: list, list2: list, list_type: str):
    """Check length of two lists match, otherwise display their content."""
    if len(list1) != len(list2):
        raise ValueError(("ERROR: Number of returned {ltype} ({}) did not "
                          "match expectation ({}). List of returned {ltype} "
                          "was {}, expected {}")
                         .format(len(list1), len(list2),
                                 list1, list2, ltype=list_type))


# test for users
print("####Testing /users")
print("Perfoming: GET on /users")
resp = requests.get(URL+"/users")
check_status_code(resp, 200)
check_app_json(resp)
check_length(resp.json()["users"], users, "users")

length = random.randint(1, len(users))
print("Performing: GET on /users?limit={}".format(length))
resp = requests.get(URL+"/users?limit={}".format(length))
check_status_code(resp, 200)
check_app_json(resp)
check_length(resp.json()["users"], users[:length], "users")


length = -1
print("Performing: GET on /users?limit={}".format(length))
resp = requests.get(URL+"/users?limit={}".format(length))
check_status_code(resp, 500)

resp = requests.get(URL+"/users?limit=1' or '1'='1")
check_status_code(resp, 500)

# test for messages
print("\n\n####Testing /messages")
print("Performing: GET on /messages")
resp = requests.get(URL + "/messages")
check_status_code(resp, 200)
check_app_json(resp)
check_length(resp.json(), msgs, "messages")

first = resp.json()[0]["name"]
print("Performing: GET on /messages?name={}".format(first))
resp = requests.post(URL + "/messages", data={'name': first})
check_status_code(resp, 200)
check_length(resp.json(), [first], "messages")

print("Performing: GET on /messages/nam=")
resp = requests.post(URL + "/messages", data={'nam': ""})
check_status_code(resp, 500)

print("Performing: POST on /messages with form-data "
      "{\"name\": \"he' OR '1'='1\"}")
resp = requests.post(URL + "/messages", data={'name': "he' OR '1'='1"})
check_status_code(resp, 200)
check_length(resp.json(), [], "messages")

print("All tests passed!")
print("GOOD")