import hug
import uuid
from db import Token, Message
import peewee


@hug.directive()
def token(request=None, **kwargs):
    return request and request.headers and request.headers['AUTHORIZATION']


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
def send_message(hug_token, message: hug.types.text):
    msg = Message.create(content=message, token=Token.get(Token.token==hug_token))
    return {"message_id": msg.id}

@hug.get(requires=token_authentication)
def receive_message(hug_token, after_msg_id: hug.types.number):
    token = Token.get(Token.token == hug_token)
    return Message.select().where(Message.token==token, Message.from_me==True, Message.id > after_msg_id)