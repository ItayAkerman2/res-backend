from . import db

class Tastes(db.Model):
    id = db.Column(db.Integer,primary_key = True,auto_increment=True)
    taste = db.Column(db.String(50),nullable=False)