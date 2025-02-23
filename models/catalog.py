from . import db
from datetime import datetime 

class Catalog(db.Model):
    __tablename__ = 'catalog'
    id = db.Column(db.Integer,primary_key=True,auto_increment = True)
    catalogName = db.Column(db.String(50),nullable = False)