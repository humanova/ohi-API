
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import os
import datetime
from psycopg2 import *
from peewee import * 

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
    account_type = IntegerField()
    last_login = DateField()
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
            with db.atomic():
                user = User.create(
                    username= username,
                    password= password,
                    account_type = acc_type,
                    email = email,
                    last_login= datetime.datetime.now(),
                    register_date= datetime.datetime.now(),
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

    