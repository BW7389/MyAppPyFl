from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    __tablename__ = 'users'
    
    # Specify length for the VARCHAR columns (username, email)
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))  # UUID for id
    username = db.Column(db.String(50), unique=True, nullable=False)  # Username with length
    email = db.Column(db.String(120), unique=True, nullable=False)    # Email with length
    password = db.Column(db.Text(), nullable=False)                   # Password field

    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self,password):
        self.password = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete():
        db.session.delete(self)
        db.session.commit()
    
