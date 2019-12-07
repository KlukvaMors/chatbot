from db import Message
from playhouse.shortcuts import model_to_dict


def process_question(message):
    return model_to_dict(Message.create(token=message.token, content='Reply to: '+message.content, reply_to=message))