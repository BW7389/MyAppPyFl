from extensions import db
from models import User

def make_shell_context():
    return {'db': db, 'User': User}
