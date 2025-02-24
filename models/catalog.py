from . import db

class Catalog(db.Model):
    catalog_id = db.Column(db.Integer,primary_key=True,auto_increment = True)
    catalogName = db.Column(db.String(50),nullable = False)