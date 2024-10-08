from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.String(dump_only=True)  
    username = fields.String(required=True, validate=validate.Length(min=1)) 
    email = fields.Email(required=True) 
