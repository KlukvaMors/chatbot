import hug
from falcon import HTTP_200, HTTP_401
import api
from db import Token
import uuid


def validate_uuid4(uuid_string):
    try:
        uuid.UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True

def test_auth():
    response = hug.test.get(api, "receive_message", headers={'Authorization': Token.get().token})
    assert response.status == HTTP_200
    response = hug.test.get(api, "receive_message")
    assert response.status == HTTP_401

def test_get_token():
    response = hug.test.get(api, "get_token")
    assert len(response.data) == 32
    assert validate_uuid4(response.data)

def test_send_message():
    response = hug.test.post(api, "send_message", headers={'Authorization': Token.get().token})

if __name__ == "__main__":
    # test_auth()
    # test_get_token()
    test_send_message()