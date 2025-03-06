from . import db

class Order_Details(db.Model):
    order_details_id = db.Column(db.Integer,primary_key = True)
    order_id = db.Column(db.Integer,db.ForeignKey('orders.orderID', ondelete="CASCADE"))
    dishID = db.Column(db.Integer,db.ForeignKey('dishes.dishID', ondelete="CASCADE"))
    number_of_dishes = db.Column(db.Integer,nullable = False) 
    price = db.Column(db.Integer)
    