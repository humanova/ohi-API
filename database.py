
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import os
import datetime
from datetime import timezone
from psycopg2 import *
from peewee import * 
from utils import str2md5

DATABASE_NAME = os.environ['DATABASE_NAME']
DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_USER = os.environ['DATABASE_USER']
DATABASE_PASS = os.environ['DATABASE_PASS']
DATABASE_HOST = os.environ['DATABASE_HOST']

db = PostgresqlDatabase(
    DATABASE_NAME,  # Required by Peewee.
    user=DATABASE_USER,  # Will be passed directly to psycopg2.
    password=DATABASE_PASS,  # Ditto.
    host=DATABASE_HOST)  # Ditto.

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    unique_id = CharField()
    hwid = CharField()
    account_type = IntegerField()
    last_login = DateField()
    sub_end_date = DateTimeField()
    sub_end_timestamp = BigIntegerField()
    register_date = DateTimeField()

class DB:

    def __init__(self):

        self.is_connected = False
    
    def InitDatabase(self):
        try:
            db.create_tables([User])
        except Exception as e:
            print("Couldn't create the tables, it may already exist on the database...")
            print(e)

    def Connect(self):

        try:
            db.connect()
            self.is_connected = True
        except:
            print(f"couldn't connect to database")
            self.is_connected = False

    def AddUser(self, username, email, password, acc_type):
        try:
            now = datetime.datetime.now()
            end_date = now
            if acc_type == 1: end_date = now + datetime.timedelta(days=30)
            elif acc_type == 2: end_date = now + datetime.timedelta(days=90)
            elif acc_type == 3: end_date = now + datetime.timedelta(days=1095)
            else: end_date = now + datetime.timedelta(days=30)
            end_timestamp = end_date.replace(tzinfo=timezone.utc).timestamp()

            with db.atomic():
                user = User.create(
                    username = username,
                    password = password,
                    account_type = acc_type,
                    unique_id = str2md5(username + email),
                    hwid = "not_set",
                    email = email,
                    last_login = now,
                    sub_end_date = end_date,
                    sub_end_timestamp = end_timestamp,
                    register_date = now,
                )
                print(f"[DB] Registered a new user -> username : {username}")
                return user
        except Exception as e:
            print(f'Error while registering a new user : {e}')
        

    def GetUser(self, user_name, password):
        try:
            user = User.select().where(User.username == user_name, User.password == password).get()
        except:
            print(f"[DB] Couldn't find any user with these credidentals : {user_name} :  {password}")
            return None
        return user

    