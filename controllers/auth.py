from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from models import User
from extensions import jwt

auth_bp = Blueprint('auth', __name__)
revoked_tokens = set()

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

@auth_bp.post('/logout')
@jwt_required()
def logout():
    jti = get_jwt()['jti']  
    revoked_tokens.add(jti) 
    return jsonify(msg="Access token has been revoked"), 200



@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']  # Get the token's jti
    return jti in revoked_tokens  # Return True if the token is revoked

def revoke_token(jti):
    revoked_tokens.add(jti) 


@auth_bp.get('/whoami')
@jwt_required()
def whoami():
    try:
        claims = get_jwt()
        return jsonify({'message': 'Here are your claims', 'claims': claims}), 200
    except ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401