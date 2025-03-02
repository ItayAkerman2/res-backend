from . import db

class Dishes_Tastes(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    dishID = db.Column(db.Integer, db.ForeignKey('dishes.dishID'),nullable=False)
    tasteID = db.Column(db.Integer, db.ForeignKey('tastes.id'),nullable=False)