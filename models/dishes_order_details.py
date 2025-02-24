from . import db 

class Dishes_Order_Details(db.Model):
    dodID = db.Column(db.Integer,primary_key = True,auto_increment = True)
    dishID = db.Column(db.Integer, db.ForeignKey('dishes.dishID'),nullable=False)
    order_detail_id = db.Column(db.Integer, db.ForeignKey('order_details.order_detail_id'),nullable=False)
    