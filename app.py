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
    username = request.form['username']
    password = request.form['password']
    pass_hash = str2md5(password)
    
    user = db.GetUser(username, pass_hash)
    if not user == None:
        user.last_login = datetime.datetime.now()
        return {'success' : 'true', 'userdata': {'username' : user.username, 'email' : user.email, 'register_date' : user.register_date}}
    else:
        return {'success' : 'false'}

@app.route('/api/v1/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    pass_hash = str2md5(password)
    
    user = db.AddUser(username, email, pass_hash)
    if not user == None:
        
        return {'success' : 'true', 'userdata': {'username' : user.username, 'email' : user.email, 'register_date' : user.register_date}}
    else:
        return {'success' : 'false'}

app.run(host=5001)