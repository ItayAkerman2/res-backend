from . import db


class Catalog_Dishes(db.Model):
    cdID = db.Column(db.Integer,primary_key = True,auto_increment = False)
    dishID = db.Column(db.Integer, db.ForeignKey('dishes.dishID'),nullable=False)
    catalogID = db.Column(db.Integer,db.ForeignKey('catalog.id'),nullable = False)
    