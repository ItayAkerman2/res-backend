from . import db

class Dish_Type(db.Model):
    __tablename__ = 'dish_type'
    id = db.Column(db.Integer,primary_key = True)
    type = db.Column(db.String(50),nullable = False)
