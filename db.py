
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from peewee import *


class BaseModel(Model):
    class Meta:
        database = MySQLDatabase("test_chat_bot", user='root', password='3616', host='127.0.0.1', port=3306)


class Token(BaseModel):
    token = CharField(max_length=32, null=False)
    expires = DateField(default=lambda: date.today() + relativedelta(years=1))
    last_visit = DateTimeField()


class Message(BaseModel):
    content = TextField(null=False)
    created = DateTimeField(default=datetime.now)
    token = ForeignKeyField(model=Token, null=False)
    reply_to = ForeignKeyField(model='self', null=True)


class Score(BaseModel):
    value = SmallIntegerField(null=False)
    message = ForeignKeyField(model=Message, null=False, unique=True)
    created = DateTimeField(default=datetime.now)
