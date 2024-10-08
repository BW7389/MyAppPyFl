from extensions import db
from uuid import uuid4

class User(db.Model):
    __tablename__ = 'users'
    
    # Specify length for the VARCHAR columns (username, email)
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))  # UUID for id
    username = db.Column(db.String(50), unique=True, nullable=False)  # Username with length
    email = db.Column(db.String(120), unique=True, nullable=False)    # Email with length
    password = db.Column(db.Text(), nullable=False)                   # Password field

    def __repr__(self):
        return f"<User {self.username}>"
