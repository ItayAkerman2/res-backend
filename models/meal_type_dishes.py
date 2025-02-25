from . import db

class Meal_Type_Dishes(db.Model):
    id = db.Column(db.Integer,primary_key = True,auto_increment = False)
    dishID = db.Column(db.Integer, db.ForeignKey('dishes.dishID'),nullable=False)
    meal_type_ID = db.Column(db.Integer,db.ForeignKey('meal_type.id'),nullable = False)