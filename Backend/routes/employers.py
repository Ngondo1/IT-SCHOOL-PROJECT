from flask import Blueprint, request, jsonify
from models import db, Employers, Users

employer_bp = Blueprint('employer_bp', __name__, url_prefix='/api/employers')

@employer_bp.route('/register', methods=['POST'])
def register_employer():
    data = request.get_json()
    required_fields = ['userID', 'companyName', 'businessType', 'registrationNumber']

    for field in required_fields:
        if field not in data or str(data[field]).strip() == '':
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    user = Users.query.filter_by(userID=data['userID']).first()
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    existing = Employers.query.filter_by(employerID=data['userID']).first()
    if existing:
        return jsonify({"message": "Employer profile already exists", "employerID": existing.employerID}), 200

    employer = Employers(
        employerID=data['userID'],
        companyName=data['companyName'],
        businessType=data['businessType'],
        registrationNumber=data['registrationNumber'],
        verified=False
    )

    try:
        db.session.add(employer)
        db.session.commit()
        return jsonify({"message": "Employer registered successfully", "employerID": employer.employerID}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500


@employer_bp.route('/update_profile', methods=['PUT'])
def update_employer_profile():
    data = request.get_json()
    employerID = data.get('employerID')

    employer = Employers.query.filter_by(employerID=employerID).first()
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    fields = ['companyName', 'businessType', 'registrationNumber']

    for field in fields:
        if field in data:
            setattr(employer, field, data[field])

    try:
        db.session.commit()
        return jsonify({"message": "Employer profile updated successfully"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500


@employer_bp.route('/<int:employerID>', methods=['GET'])
def get_employer_profile(employerID):
    employer = Employers.query.filter_by(employerID=employerID).first()
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    profile = {
        "employerID": employer.employerID,
        "companyName": employer.companyName,
        "businessType": employer.businessType,
        "registrationNumber": employer.registrationNumber,
        "verified": employer.verified
    }

    return jsonify(profile), 200