from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from database import db



# users = {
#     'user1': {'password': 'password1'},
#     'user2': {'password': 'password2'}
# }

auth = Blueprint('auth', __name__)

@auth.route('/a', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'}), 200

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # user already exists
    user = db.get_user(username)
    if user:
        return jsonify({'error': 'User already exists'}), 400
    
    db.add_user(username, password)
    return jsonify({'message': 'User created'}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    username = data.get('username')
    password = data.get('password')
    print(username)

    # no user
    user = db.get_user(username)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # wrong password
    if user['password'] != password:
        return jsonify({'error': 'Wrong password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Logged in as {current_user}'}), 200

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200
