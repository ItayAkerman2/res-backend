from . import db

class Dishes(db.Model):
    dishID = db.Column(db.Integer,primary_key = True)
    dishName = db.Column(db.String(50))
    cost = db.Column(db.Numeric(precision = 10,scale = 2))
    cook_time = db.Column(db.TIMESTAMP())
    image_url = db.Column(db.String(255))
    description = db.Column(db.String(255))
    to_show = db.Column(db.Integer)
    created_at = db.Column(db.Date)
