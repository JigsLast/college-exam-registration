from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import re
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# MongoDB connection with error handling
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.server_info()  # Test connection
    db = client['student_registration_db']
except Exception as e:
    print("MongoDB connection error:", e)
    exit(1)

@app.route('/api/students', methods=['GET', 'POST'])
def handle_students():
    if request.method == 'POST':
        # Input validation
        required_fields = ['name', 'age', 'mobile_no', 'roll_no', 'stream', 'subjects']
        if not all(field in request.json for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Validate data types
        try:
            if not isinstance(request.json['subjects'], list):
                return jsonify({'error': 'Subjects must be an array'}), 400
                
            if not re.match(r'^[6-9]\d{9}$', request.json['mobile_no']):
                return jsonify({'error': 'Invalid Indian mobile number'}), 400

            student = {
                'name': request.json['name'],
                'age': int(request.json['age']),
                'mobile_no': request.json['mobile_no'],
                'roll_no': request.json['roll_no'],
                'stream': request.json['stream'],
                'subjects': request.json['subjects'],
                'registered_at': datetime.now()
            }

            # Insert with error handling
            result = db.students.insert_one(student)
            return jsonify({
                'status': 'success',
                'inserted_id': str(result.inserted_id),
                'student': student  # Return the created student for verification
            }), 201

        except ValueError as e:
            return jsonify({'error': f'Invalid data format: {str(e)}'}), 400

    elif request.method == 'GET':
        try:
            # Convert MongoDB documents to JSON-serializable format
            students = list(db.students.find({}))
            
            # Convert ObjectId to string and ensure subjects exists
            for student in students:
                student['_id'] = str(student['_id'])
                student.setdefault('subjects', [])  # Ensure subjects exists
                
            return jsonify(students)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'database': 'connected' if client else 'disconnected'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)