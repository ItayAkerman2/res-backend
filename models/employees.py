from . import db

class Employees(db.Model):
    employee_id = db.Column(db.Integer,primary_key=True,auto_increment=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name=db.Column(db.String(50),nullable=False)
    pay_per_hour=db.Column(db.Numeric(precision = 10,scale = 2),nullable = False)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.role_id'))