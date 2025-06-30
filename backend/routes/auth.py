from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User
from backend.db_session import Session
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'msg': 'Missing required fields'}), 400
    session = Session()
    if session.query(User).filter((User.username == username) | (User.email == email)).first():
        session.close()
        return jsonify({'msg': 'Username or email already exists'}), 409
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(username=username, email=email, password=hashed_pw)
    session.add(user)
    session.commit()
    access_token = create_access_token(identity=str(user.user_id))
    session.close()
    return jsonify(access_token=access_token), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and user.password and (bcrypt.checkpw(password.encode(), user.password.encode()) if user.password.startswith('$2b$') else user.password == password):
        access_token = create_access_token(identity=str(user.user_id))
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Bad username or password'}), 401
