from . import db

class Meal_Type_Dishes(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    dishID = db.Column(db.Integer, db.ForeignKey('dishes.dishID', ondelete="CASCADE"),nullable=False)
    meal_type_ID = db.Column(db.Integer,db.ForeignKey('meal_type.id', ondelete="CASCADE"),nullable = False)
    