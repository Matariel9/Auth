from marshmallow import Schema, fields
from setup_db import db

class Auth(db.Model):
    __tablename__ = 'Auth'
    userid = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.Integer)
    refresh_token = db.Column(db.Integer)

class AuthSchema(Schema):
    access_token = fields.Int()
    refresh_token = fields.Int()
