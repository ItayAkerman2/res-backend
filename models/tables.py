from . import db

class Tables(db.Model):
    table_id = db.Column(db.Integer,primary_key = True,auto_increment = True)
    guests_amount = db.Column(db.Integer,nullable = False)