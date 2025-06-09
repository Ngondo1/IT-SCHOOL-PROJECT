from flask import Blueprint, request, jsonify
from models import db, Users
from datetime import datetime

employee_bp = Blueprint('employee_bp', __name__, url_prefix='/api/employees')

@employee_bp.route('/register', methods=['POST'])
def register_employee():
    data = request.get_json()
    phone = data.get('phoneNo', '').strip()

    if not phone:
        return jsonify({"error": "phoneNo is required"}), 400

    existing = Users.query.filter_by(phoneNo=phone).first()
    if existing:
        return jsonify({"message": "Employee already exists", "userID": existing.userID}), 200

    new_employee = Users(
        phoneNo=phone,
        RegistrationTime=datetime.utcnow(),
        Name='Unknown',
        Age=0,
        Gender='Unknown',
        County='Unknown',
        Town='Unknown',
        LevelOfEducation='Unknown',
        Profession='Unknown',
        MaritalStatus='Unknown',
        Religion='Unknown',
        Ethnicity='Unknown',
        Description='No description provided'
    )

    try:
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({"message": "Employee registered", "userID": new_employee.userID}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to register employee"}), 500


@employee_bp.route('/update_profile', methods=['PUT'])
def update_employee_profile():
    data = request.get_json()
    phone = data.get('phoneNo', '').strip()

    if not phone:
        return jsonify({"error": "phoneNo is required"}), 400

    employee = Users.query.filter_by(phoneNo=phone).first()
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    fields = [
        'Name', 'Age', 'Gender', 'County', 'Town',
        'LevelOfEducation', 'Profession', 'MaritalStatus',
        'Religion', 'Ethnicity', 'Description'
    ]

    for field in fields:
        if field in data:
            setattr(employee, field, data[field])

    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully!"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to update profile"}), 500


@employee_bp.route('/by_phone', methods=['GET'])
def get_employee_by_phone():
    phone = request.args.get('phoneNo', '').strip()
    if not phone:
        return jsonify({"error": "Missing phone number"}), 400

    employee = Users.query.filter_by(phoneNo=phone).first()
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({
        "userID": employee.userID,
        "Name": employee.Name,
        "phoneNo": employee.phoneNo,
        "Profession": employee.Profession
    }), 200


@employee_bp.route('/<int:user_id>/profile', methods=['GET'])
def get_employee_profile(user_id):
    employee = Users.query.filter_by(userID=user_id).first()
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    profile = {
        "userID": employee.userID,
        "Name": employee.Name,
        "Age": employee.Age,
        "Gender": employee.Gender,
        "County": employee.County,
        "Town": employee.Town,
        "LevelOfEducation": employee.LevelOfEducation,
        "Profession": employee.Profession,
        "MaritalStatus": employee.MaritalStatus,
        "Religion": employee.Religion,
        "Ethnicity": employee.Ethnicity,
        "Description": employee.Description
    }
    return jsonify(profile), 200