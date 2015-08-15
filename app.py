from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_user
from flask.ext.cors import CORS 
from flask.ext.sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "*", "methods": "*"}})
cors = CORS(app)
app.debug = True
app.config.from_object('config')
app.config['SECRET_KEY'] = 'super-secret'
db = SQLAlchemy(app)
from models import *
db.create_all()


jwt = JWT(app)

@jwt.authentication_handler
def authenticate(username, password):
    u = User.query.filter_by(username=username, password=password).first()
    if u:
        return u

@jwt.user_handler
def load_user(payload):
    print "LOAD USER "
    print payload['user_id']
    u = User.query.get(payload['user_id'])
    return u

@app.route('/protected')
@jwt_required()
def protected():
    return 'Success! current user id is '+str(current_user.id)

# Registration
@app.route('/api/v1/users', methods=['POST'])
def register():
    user = request.get_json()['user']
    username = user['username']
    email    = user['email']
    password = user['password']
    u = User(username=username, email=email, password=password)
    db.session.add(u)
    db.session.commit()
    result = {}
    result['username'] = username
    result['email']    = email
    result['password'] = password
    return json.dumps(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
