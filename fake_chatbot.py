from db import Message


def process_question(message):
    return Message.create(token=message.token, content='Reply to: '+message.content, reply_to=message).dicts()