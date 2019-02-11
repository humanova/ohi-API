import flask
import datetime
from flask import request, jsonify
import database
import hashlib

def str2md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

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
        return jsonify(dict(success=True,userdata=dict(username=user.username,email=user.email,account_type = user.account_type, register_date=user.register_date)))
    else:
        return jsonify(dict(success=False))

@app.route('/api/v1/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    email = request.form['email']
    pass_hash = str2md5(password)
    
    user = db.AddUser(username, email, pass_hash)
    if not user == None:
        
        return jsonify(dict(success=True,userdata=dict(username=user.username,email=user.email,register_date=user.register_date)))
    else:
        return jsonify(dict(success=False))

app.run(host='0.0.0.0', port='80')