from . import db

class Employees_Tables(db.Model):
    employee_table_id = db.Column(db.Integer,primary_key=True,auto_increment=True)
    employee_id = db.Column(db.Integer,db.ForeignKey('employees.employee_id'),nullable=False)
    table_id = db.Column(db.Integer,db.ForeignKey('tables.table_id'))