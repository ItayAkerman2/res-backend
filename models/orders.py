from . import db

class Orders(db.Model):
    orderID = db.Column(db.Integer,primary_key = True,auto_increment = True)
    order_time = db.Column(db.DateTime,nullable = False)
    to_show = db.Column(db.Integer)