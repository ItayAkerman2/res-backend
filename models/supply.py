from . import db

class Supply(db.Model):
    supply_id = db.Column(db.Integer,primary_key = True,auto_increment=True)
    name = db.Column(db.String(50),nullable = False)
    available = db.Column(db.Integer,nullable=False,default=0)
    price = db.Column(db.Integer,nullable=False)