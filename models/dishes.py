from . import db

class Dishes(db.Model):
    dishID = db.Column(db.Integer,primary_key = True,auto_increment = True)
    dishName = db.Column(db.String(50),nullable = False)
    cost = db.Column(db.Numeric(precision = 10,scale = 2),nullable = False)