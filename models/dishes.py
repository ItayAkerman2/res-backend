from . import db

class Dishes(db.Model):
    dishID = db.Column(db.Integer,primary_key = True,auto_increment = True)
    dishName = db.Column(db.String(50),nullable = False)
    cost = db.Column(db.Numeric(precision = 10,scale = 2),nullable = False)
    cook_time = db.Column(db.DateTime,nullable = False)
    image_url = db.Column(db.String(255),nullable=False)
    description = db.Column(db.String(255))
    to_show = db.Column(db.Integer)
    created_at = db.Column(db.Date)
