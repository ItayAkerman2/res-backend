from . import db

class Orders(db.Model):
    orderID = db.Column(db.Integer,primary_key = True,auto_increment = True)
    order_time = db.Column(db.DateTime,nullable = False)
    table_id = db.Column(db.Integer,db.ForeignKey('tables.table_id'))