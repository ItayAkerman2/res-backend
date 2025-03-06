from . import db

class Dish_Type_Dish(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    dishID =  db.Column(db.Integer,db.ForeignKey('dishes.dishID', onelete="CASCADE"))
    dish_type_id = db.Column(db.Integer,db.ForeignKey('dish_type.id', onelete="CASCADE"))