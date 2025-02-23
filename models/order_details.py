from . import db

class Order_Details(db.Model):
    order_details_id = db.Column(db.Integer,primary_key = True,auto_increment = True)
    number_of_dishes = db.Column(db.Integer,nullable = False)
    