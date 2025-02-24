from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import requests
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db:3306/res'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

limiter = Limiter(app, key_func=get_remote_address)


def serialize_model(instance):
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

@app.route('/employees', methods=['GET'])
def load_employees():
    try:
        employees = Employee.query.all()
        return jsonify([serialize_model(emp) for emp in employees]), 200
    except SQLAlchemyError as SQ_Er:
        logger.error(f"Database error: {SQ_Er}", exc_info=True)
        return jsonify({'error': 'Database error occurred'}), 500

@app.route('/tables', methods=['GET'])
def load_tables():
    try:
        tables = Table.query.all()
        return jsonify([serialize_model(table) for table in tables]), 200
    except SQLAlchemyError as SQ_Er:
        logger.error(f"Database error: {SQ_Er}", exc_info=True)
        return jsonify({'error': f'Database error occurred -/ {SQ_Er}'}), 500

@app.route('/dis', methods=['GET'])
def load_dis():
    try:
        dis_list = Dis.query.all()
        return jsonify([serialize_model(dis) for dis in dis_list]), 200
    except SQLAlchemyError as SQ_Er:
        logger.error(f"Database error: {SQ_Er}", exc_info=True)
        return jsonify({'error': f'Database error occurred -/ {SQ_Er}'}), 500

@app.route('/dis', methods=['POST'])
@limiter.limit("10 per minute")  
def add_dis():
    try:
        data = request.get_json()
        new_dis = Dis(**data)
        db.session.add(new_dis)
        db.session.commit()
        return jsonify(serialize_model(new_dis)), 201
    except SQLAlchemyError as SQ_Er:
        db.session.rollback()
        logger.error(f"Database error: {SQ_Er}", exc_info=True)
        return jsonify({'error': f'Database error occurred /- {SQ_Er}'}), 500

@limiter.limit("10 per minute")  
def add_table():
    try:
        data = request.get_json()
        new_table = Tables(**data)
        db.session.add(new_table)
        db.session.commit()
        return jsonify(serialize_model(new_table)),201
    except SQLAlchemyError as SQ_Er:
        db.session.rollback()
        logger.error(f"Error with sqlalchemy -- {SQ_Er}", exc_info=True)
        return jsonify({'error': f'Connection error / - {SQ_Er}'})

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
        db.session.commit()
        return jsonify({'message': f'Dis {dis_id} removed successfully'}), 200
    except SQLAlchemyError as SQ_Er:
        db.session.rollback()
        logger.error(f"Database error: {SQ_Er}", exc_info=True)
        return jsonify({'error': f'Database error occurred -/ {SQ_Er}'}), 500

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
        db.session.commit()
        return jsonify({'message': f'Order {order_id} removed successfully'}), 200
    except SQLAlchemyError as SQ_Er:
        db.session.rollback()
        logger.error(f"Database error: {SQ_Er}", exc_info=True)
        return jsonify({'error': f'Database error occurred -/ {SQ_Er}'}), 500


##helper functions
##note , i have created two endpoints for those two function 

#this is for checking database connectivity to the backend
@app.route('/health', methods=['GET'])
@limiter.limit("10 per minute")
def check_database_connection():
    try:
        db.session.execute('SELECT 1')
        db_status = "healthy"
    except SQLAlchemyError as SQ_Er:
        logger.error(f"Database connection error: {SQ_Er}", exc_info=True)
        db_status = "unhealthy"
    
    return jsonify({"database_status": db_status}), 200 if db_status == "healthy" else 500

#this is for checking front end connectivity health to the backend 
@app.route('/frontend-health', methods=['GET'])
@limiter.limit("10 per minute")
def check_frontend_connection():
    try:
        frontend_url = "http://localhost:5000" 
        response = requests.get(frontend_url + "/health")
        if response.status_code == 200:
            frontend_status = "healthy"
        else:
            frontend_status = "unhealthy"
    except requests.exceptions.RequestException as e:
        logger.error(f"Frontend connection error: {e}", exc_info=True)
        frontend_status = "unhealthy"
    
    return jsonify({
        "status": frontend_status,
        "message": "Backend is reachable from the frontend." if frontend_status == "healthy" else "Backend or frontend is unreachable."
    }), 200 if frontend_status == "healthy" else 500

def log_to_file():
    handler = logging.FileHandler('change me') ## Add a path here to store the logs
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

##note here you will need to create the admin user
if __name__ == '__main__':
    log_to_file()
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
