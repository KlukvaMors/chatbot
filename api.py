import hug
import uuid
from db import Token, Message, Score, User
import peewee
import fake_chatbot as chatbot
from falcon import HTTP_404, HTTP_409, HTTP_422, HTTPError
import hashlib


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
def get_new_token():
    token = uuid.uuid4().hex
    Token.create(token=token)
    return {'token': token}


@hug.post()
def registration(login: hug.types.text, password: hug.types.text):

    if len(password) >= 6:
        password = hashlib.sha1(password.encode()).hexdigest()
    else:
        raise HTTPError(HTTP_422)

    token = uuid.uuid4().hex
    token = Token.create(token=token)
    try:
        User.create(**locals())
    except peewee.IntegrityError:
        token.delete()
        raise HTTPError(HTTP_409)
    return {'status': 'ok'}


@hug.get()
def get_token(login: hug.types.text, password: hug.types.text):
    try:
        user = User.get(login=login,
                        password=hashlib.sha1(password.encode()).hexdigest())
        return {'token': user.token.token}
    except User.DoesNotExist:
        raise HTTPError(HTTP_404)


@hug.post(requires=token_authentication)
def send_message(hug_token, message: hug.types.text):
    msg = Message.create(content=message, token=Token.get(Token.token == hug_token))
    rpl_msg = chatbot.process_question(msg)
    return {"content": rpl_msg.content, "created": rpl_msg.created}


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
    except Message.DoesNotExist:
        raise HTTPError(HTTP_404)
    except peewee.IntegrityError:
        raise HTTPError(HTTP_409)
