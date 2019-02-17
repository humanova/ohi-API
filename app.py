import os
import flask
import datetime
from flask import request, jsonify
import database
from database import User
import json
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

from utils import str2md5, isexpired

db = database.DB()
db.Connect()
try:
    db.InitDatabase()
except Exception as e:
    print(e)

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route('/api/v1/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    pass_hash = str2md5(password)
    
    user = db.GetUser(username, pass_hash)

    if not user == None:
        user.last_login = datetime.datetime.now()
        is_expired = isexpired(user.last_login, user.sub_end_date)

        return jsonify(dict(success=True,userdata=dict(username=user.username,email=user.email,account_type = user.account_type, unique_id = user.unique_id, is_expired = is_expired, sub_end_date = user.sub_end_date, sub_end_timestamp = user.sub_end_timestamp, register_date=user.register_date)))
    else:
        return jsonify(dict(success=False))

@app.route('/api/v1/app_login', methods=['POST'])
def app_login():
    username = request.json['username']
    password = request.json['password']
    hwid = request.json['hwid']
    pass_hash = str2md5(password)
    
    user = db.GetUser(username, pass_hash)

    if not user == None:
        user.hwid = hwid
        user.last_login = datetime.datetime.now()
        is_expired = isexpired(user.last_login, user.sub_end_date)

        return jsonify(dict(success=True,userdata=dict(username=user.username,email=user.email,account_type = user.account_type, unique_id = user.unique_id, is_expired = is_expired, sub_end_date = user.sub_end_date, sub_end_timestamp = user.sub_end_timestamp, register_date=user.register_date)))
    else:
        return jsonify(dict(success=False))

@app.route('/api/v1/register', methods=['POST'])
def register():
    api_key = request.json['api_key']
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    pass_hash = str2md5(password)
    
    key = db.CheckKey("api_key", api_key)
    if key:
        user = db.AddUser(username, email, pass_hash, 1)
        if not user == None:
            return jsonify(dict(success=True,userdata=dict(username=user.username,email=user.email, unique_id = user.unique_id, register_date=user.register_date)))
        else:
            return jsonify(dict(success=False))
    else:
        return jsonify(dict(success=False))

@app.route('/api/v1/users', methods=['POST'])
def get_users():
    api_key = request.json['api_key']
    key = db.CheckKey("api_key", api_key)
    if key:
        users = db.GetUsers()
        if not len(users) == 0:
            users_dictArr = []
            for user in users:
                users_dictArr.append(model_to_dict(user))
            return jsonify(dict(success=True, data=users_dictArr))
        else:
            return jsonify(dict(success=False))
    else:
        return jsonify(dict(success=False))


@app.route('/api/v1/edit_user', methods=['POST'])
def edit_user():
    api_key = request.json['api_key']
    user_data_dict = request.json['user_data']
    
    key = db.CheckKey("api_key", api_key)
    if key:
        new_user_data = json.dumps(dict_to_model(User, user_data_dict))
        user = db.SuperGetUser(new_user_data.unique_id)
        if not user == None:
            try:
                user = new_user_data
            except:
                return jsonify(dict(success=False))
            user_json = json.dumps(model_to_dict(user))
            return jsonify(dict(success=True, data=user_json))
        else:
            return jsonify(dict(success=False))
    else:
        return jsonify(dict(success=False))        
app.run(host='0.0.0.0', port=os.environ['PORT'])
