import hug
import uuid
from db import Token, Message, Score
import peewee
import fake_chatbot as chatbot


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
    msg = Message.create(content=message, token=Token.get(Token.token == hug_token))
    chatbot.process_question(msg)
    return {"message_id": msg.id}


@hug.get(requires=token_authentication)
def receive_message(hug_token, after_msg_id: hug.types.number):
    token = Token.get(Token.token == hug_token)
    return Message.select().where(Message.token == token, Message.reply_to != None, Message.id > after_msg_id).dicts()


@hug.post(requires=token_authentication)
def score_message(hug_token, message_id: hug.types.number, score: hug.types.number):
    try:
        msg = Message.get(Message.token == Token.get(Token.token == hug_token),
                          Message.id == message_id,
                          Message.reply_to != None)
        Score.create(message=msg, value=score)
        return {"status": "ok"}
    except peewee.DoesNotExist:
        return {"error": "Wrong message_id"}
    except peewee.IntegrityError:
        return {"error": "Score has already set"}
