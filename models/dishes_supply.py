from . import db

class Dishes_Supply(db.Model):
    dsID = db.Column(db.Integer,primary_key=True,auto_increment=True)
    supplyID = db.Column(db.Integer,db.ForeignKey('supply.supply_id'))
    dishID = db.Column(db.Integer,db.ForeignKey('dishes.dishID'))
