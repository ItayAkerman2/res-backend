from . import db

class Order_Details(db.Model):
    order_details_id = db.Column(db.Integer,primary_key = True,auto_increment = True)
    order_id = db.Column(db.Integer,db.ForeignKey('orders.orderID'))
    dishID = db.Column(db.Integer,db.ForeignKey('dishes.dishID')) 
    number_of_dishes = db.Column(db.Integer,nullable = False) 
    price = db.Column(db.Integer)
    