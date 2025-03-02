from . import db

class Roles(db.Model):
    role_id = db.Column(db.Integer,primary_key=True)
    role_name=db.Column(db.String(50),nullable=False)