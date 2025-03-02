from . import db

class Dish_Type(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    type = db.Column(db.String(50),nullable = False)
    