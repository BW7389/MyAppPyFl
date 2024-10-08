from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/register')
def register_user():
    
    data = request.get_json()
    user = User.get_user_by_username(username = data.get('username'))
    
    if user is not None:
        return jsonify({'error': 'User already exists'}, 403)
    
    new_user = User(
        username = data.get('username'), 
        email = data.get('email')
    )
    
    new_user.set_password(password= data.get('password'))
    new_user.save()
    
    return jsonify({'message': 'User registered successfully'}, 201)


@auth_bp.post('/login')
def login_user():
    
    data = request.get_json()
    
    user = User.get_user_by_username(username = data.get('username'))
    
    if user and (user.check_password(password= data.get('password'))):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)
        return jsonify(
                        {
                            'message': 'Login successful',
                            'tokens': {
                                'access_token': access_token,
                                'refresh_token': refresh_token
                            }
                        }, 200)
    return jsonify({'error': 'Invalid username or password'}, 400)


@auth_bp.get('/whoami')
@jwt_required()
def whoami():
    return jsonify({'message': 'message '}), 200