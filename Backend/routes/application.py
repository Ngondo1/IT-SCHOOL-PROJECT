from flask import Blueprint, request, jsonify
from models import db, Applications, Jobs, Users
from datetime import datetime

application_bp = Blueprint('application_bp', __name__, url_prefix='/api/applications')

@application_bp.route('/apply', methods=['POST'])
def apply_to_job():
    data = request.get_json()
    required_fields = ['jobID', 'applicantID']

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    job = Jobs.query.filter_by(jobID=data['jobID'], status='active').first()
    if not job:
        return jsonify({"error": "Job not found or is no longer active."}), 404

    applicant = Users.query.filter_by(userID=data['applicantID']).first()
    if not applicant:
        return jsonify({"error": "Applicant not found."}), 404

    existing_application = Applications.query.filter_by(jobID=data['jobID'], applicantID=data['applicantID']).first()
    if existing_application:
        return jsonify({"error": "You have already applied for this job."}), 409

    application = Applications(
        jobID=data['jobID'],
        applicantID=data['applicantID'],
        applicationDate=datetime.utcnow(),
        status='pending'
    )

    try:
        db.session.add(application)
        db.session.commit()
        return jsonify({"message": "Application submitted successfully!", "applicationID": application.applicationID}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@application_bp.route('/status/<int:applicant_id>', methods=['GET'])
def get_application_status(applicant_id):
    try:
        applications = Applications.query.filter_by(applicantID=applicant_id).all()

        data = []
        for app in applications:
            job = Jobs.query.get(app.jobID)
            data.append({
                "applicationID": app.applicationID,
                "jobTitle": job.jobTitle if job else "Unknown",
                "status": app.status,
                "appliedOn": app.applicationDate
            })

        return jsonify({"applications": data}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to retrieve application status"}), 500

@application_bp.route('/update_status', methods=['POST'])
def update_application_status():
    data = request.get_json()
    required_fields = ['applicationID', 'status']

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    if data['status'] not in ['pending', 'shortlisted', 'rejected', 'hired']:
        return jsonify({"error": "Invalid status value."}), 400

    application = Applications.query.get(data['applicationID'])
    if not application:
        return jsonify({"error": "Application not found."}), 404

    application.status = data['status']

    try:
        db.session.commit()
        return jsonify({"message": f"Application status updated to '{data['status']}' successfully."}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500
