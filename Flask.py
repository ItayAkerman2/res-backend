from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
import requests
from sqlalchemy.exc import SQLAlchemyError
#from models import Employee, Order, OrderDetails, Table, Dis,db
import jwt
import os
from functools import wraps
from flask_migrate import Migrate



SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db:3306/res'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

limiter = Limiter(app)
def serialize_model(instance):
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

def handle_db_error(error):
    return jsonify({'error': f'Database error occurred {error}'}), 500

def commit_changes():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_db_error(e)

@app.route('/employees', methods=['GET'])
def load_employees():
    try:
        employees = Employee.query.all()
        return jsonify([serialize_model(emp) for emp in employees]), 200
    except SQLAlchemyError as e:
        return handle_db_error(e)

@app.route('/ordersDetails', methods=['GET'])
def load_order_details():
    try:
        order_details = OrderDetails.query.all()
        return jsonify([serialize_model(order) for order in order_details]), 200
    except SQLAlchemyError as e:
        return handle_db_error(e)

@app.route('/tables', methods=['GET'])
def load_tables():
    try:
        tables = Table.query.all()
        return jsonify([serialize_model(table) for table in tables]), 200
    except SQLAlchemyError as e:
        return handle_db_error(e)

@app.route('/dis', methods=['GET'])
def load_dis():
    try:
        dis_list = Dis.query.all()
        return jsonify([serialize_model(dis) for dis in dis_list]), 200
    except SQLAlchemyError as e:
        return handle_db_error(e)

@app.route('/dis', methods=['POST'])
@limiter.limit("10 per minute")  
def add_dis():
    try:
        data = request.get_json()
        new_dis = Dis(**data)
        db.session.add(new_dis)
        commit_changes()
        return jsonify(serialize_model(new_dis)), 201
    except SQLAlchemyError as e:
        return handle_db_error(e)

@app.route('/tables', methods=['POST'])
@limiter.limit("10 per minute")  
def add_table():
    try:
        data = request.get_json()
        new_table = Table(**data)
        db.session.add(new_table)
        commit_changes()
        return jsonify(serialize_model(new_table)), 201
    except SQLAlchemyError as e:
        return handle_db_error(e)

@app.route('/employees', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        new_employee = Employee(**data)
        db.session.add(new_employee)
        commit_changes()
        return jsonify(serialize_model(new_employee)), 201
    except SQLAlchemyError as e:
        return handle_db_error(e)

@app.route('/dis', methods=['DELETE'])
@limiter.limit("10 per minute")  
def remove_dis():
    try:
        data = request.get_json()
        dis_id = data.get('id')
        dis = Dis.query.get(dis_id)
        if dis is None:
            return jsonify({'error': 'Dis not found'}), 404

        db.session.delete(dis)
        commit_changes()
        return jsonify({'message': f'Dis {dis_id} removed successfully'}), 200
    except SQLAlchemyError as e:
        return handle_db_error(e)

@app.route('/orders', methods=['DELETE'])
@limiter.limit("10 per minute")  
def remove_order():
    try:
        data = request.get_json()
        order_id = data.get('id')
        order = Order.query.get(order_id)
        if order is None:
            return jsonify({'error': 'No order found with the given ID'}), 404

        db.session.delete(order)
        commit_changes()
        return jsonify({'message': f'Order {order_id} removed successfully'}), 200
    except SQLAlchemyError as e:
        return handle_db_error(e)

@app.route('/tables', methods=['DELETE'])
@limiter.limit("10 per minute")
def remove_table():
    try:
        data = request.get_json()
        table_id = data.get('id')
        table = Table.query.get(table_id)
        if table is None:
            return jsonify({'error': 'No table found with the given ID'}), 404

        db.session.delete(table)
        commit_changes()
        return jsonify({'message': f'Table {table_id} removed successfully'}), 200
    except SQLAlchemyError as e:
        return handle_db_error(e)    

@app.route('/employees', methods=['DELETE'])
@limiter.limit("10 per minute")
def remove_employee():
    try:
        data = request.get_json()
        employee_id = data.get('id')
        employee = Employee.query.get(employee_id)
        if employee is None:
            return jsonify({'error': 'No employee found with the given ID'}), 404

        db.session.delete(employee)
        commit_changes()
        return jsonify({'message': f'Employee {employee_id} removed successfully'}), 200
    except SQLAlchemyError as e:
        return handle_db_error(e)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required!'}), 400

    user = Employee.query.filter_by(username=data['username']).first()

    if user and user.password == data['password']: 
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401




@app.route('/health', methods=['GET'])
@limiter.limit("10 per minute")
def check_database_connection():
    try:
        db.session.execute('SELECT 1')
        db_status = "healthy"
    except SQLAlchemyError as e:
        print(f"Database connection error: {e}", exc_info=True)
        db_status = "unhealthy"
    
    return jsonify({"database_status": db_status}), 200 if db_status == "healthy" else 500

@app.route('/frontend-health', methods=['GET'])
@limiter.limit("10 per minute")
def check_frontend_connection():
    try:
        frontend_url = "https://localhost:5000" 
        response = requests.get(frontend_url + "/health")
        if response.status_code == 200:
            frontend_status = "healthy"
        else:
            frontend_status = "unhealthy"
    except requests.exceptions.RequestException as e:
        print(f"Frontend connection error: {e}", exc_info=True)
        frontend_status = "unhealthy"
    
    return jsonify({
        "status": frontend_status,
        "message": "Backend is reachable from the frontend." if frontend_status == "healthy" else "Backend or frontend is unreachable."
    }), 200 if frontend_status == "healthy" else 500

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = Employee.query.filter_by(id=data['id']).first()
            if current_user is None:
                print("User not found")
                return jsonify({'message': 'User not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(current_user, *args, **kwargs)
    return decorator



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('certificate.crt', 'private.key'))

