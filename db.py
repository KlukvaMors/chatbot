from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import configparser
from peewee import *

CONFIG_FILE = 'config.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

if 'database' not in config:
    raise Exception(f'In config file {CONFIG_FILE} must be section [database]')

db = MySQLDatabase(config['database']['database_name'],
                   user=config['database']['user'],
                   password=config['database']['password'],
                   host=config['database']['host'],
                   port=int(config['database']['port']))


class BaseModel(Model):
    class Meta:
        database = db


class Token(BaseModel):
    token = CharField(max_length=32, null=False)
    expires = DateField(default=lambda: date.today() + relativedelta(years=1))
    last_visit = DateTimeField()


class User(BaseModel):
    login = CharField(max_length=256, null=False, unique=True)
    password = CharField(null=False)
    token = ForeignKeyField(Token, null=False, unique=True)


class Message(BaseModel):
    content = TextField(null=False)
    created = DateTimeField(default=datetime.now)
    token = ForeignKeyField(model=Token, null=False)
    reply_to = ForeignKeyField(model='self', null=True)


class Score(BaseModel):
    value = SmallIntegerField(null=False)
    message = ForeignKeyField(model=Message, null=False, unique=True)
    created = DateTimeField(default=datetime.now)


if __name__ == '__main__':
    db.connect()
    db.create_tables([Token, Message, Score, User], safe=True)
    db.close()
