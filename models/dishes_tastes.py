from . import db

class Dishes_Tastes(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    dishID = db.Column(db.Integer, db.ForeignKey('dishes.dishID', ondelete="CASCADE"),nullable=False)
    tasteID = db.Column(db.Integer, db.ForeignKey('tastes.id', ondelete="CASCADE"),nullable=False)