from . import db

class Admins(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_name = db.Column(db.String(256))
    password = db.Column(db.String(256))