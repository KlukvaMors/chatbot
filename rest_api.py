import hug
import uuid
from db import Token, Message
import peewee




@hug.authentication.token
def token_authentication(token):
    try:
        Token.get(Token.token == token)
        return True
    except peewee.DoesNotExist:
        return False

@hug.get()
def get_token():
    token = uuid.uuid4().hex
    Token.create(token=token)
    return token

@hug.post(requires=token_authentication)
def send_message(request):
    print(request)
    return {"status": "ok"}