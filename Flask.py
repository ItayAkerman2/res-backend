
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/api/dis', methods=['GET'])
def load_dis():
    try:
        result = db.engine.execute("SELECT * FROM dis")
        data = [dict(row) for row in result]
        return jsonify({"data": data})
    except Exception as e:
        return (str(e))
@app.route('/api/tables', methods=['GET'])
def load_tables():
    try:
        result = db.engine.execute("SELECT * FROM tables")
        data = [dict(row) for row in result]
        return jsonify({"data": data})
    except Exception as e:
        return (str(e))
@app.route('/api/employees', methods=['GET'])
def load_employees():
    try:
        result = db.engine.execute("SELECT * FROM employees")
        data = [dict(row) for row in result]
        return jsonify({"data": data})
    except Exception as e:
        return (str(e))
    
@app.route('/api/employees', methods=['POST'])
def add_dis():
    pass



    
