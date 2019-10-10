from db import Message


def process_question(message):
    Message.create(token=message.token, content='ОТвет на: '+message.content, reply_to=message)