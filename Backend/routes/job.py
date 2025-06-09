from flask import Blueprint, request, jsonify
from models import db, Jobs
from datetime import datetime

job_bp = Blueprint('job_bp', __name__, url_prefix='/api/jobs')

ALLOWED_SKILLS = ['plumber', 'electrician', 'carpenter']
ALLOWED_LOCATIONS = [
    'westlands', 'langata', 'lavington', 'kibera',
    'karen', 'kawangware', 'gigiri', 'ruaka'
]

@job_bp.route('/post', methods=['POST'])
def post_job():
    data = request.get_json()
    required_fields = ['employerID', 'jobTitle', 'jobDescription', 'jobLocation', 'employmentType']

    for field in required_fields:
        if field not in data or not data[field].strip():
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    location = data['jobLocation'].strip().lower()
    title = data['jobTitle'].strip().lower()

    if location not in ALLOWED_LOCATIONS:
        return jsonify({"error": f"Invalid location. Allowed options: {', '.join(ALLOWED_LOCATIONS)}"}), 400

    if not any(skill in title for skill in ALLOWED_SKILLS):
        return jsonify({"error": f"Job title must include one of: {', '.join(ALLOWED_SKILLS)}"}), 400

    new_job = Jobs(
        employerID=data['employerID'],
        jobTitle=data['jobTitle'].strip(),
        jobDescription=data['jobDescription'].strip(),
        jobLocation=location,
        salaryRange=data.get('salaryRange', 'Negotiable'),
        employmentType=data['employmentType'].strip(),
        postDate=datetime.utcnow(),
        status='active'
    )

    try:
        db.session.add(new_job)
        db.session.commit()
        return jsonify({"message": "Job posted successfully!", "jobID": new_job.jobID}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@job_bp.route('/', methods=['GET'])
def get_filtered_jobs():
    location = request.args.get('location', '').strip().lower()
    skill = request.args.get('skill', '').strip().lower()

    try:
        query = Jobs.query.filter_by(status='active')

        if location:
            if location not in ALLOWED_LOCATIONS:
                return jsonify({"error": f"Invalid location. Choose from: {', '.join(ALLOWED_LOCATIONS)}"}), 400
            query = query.filter(Jobs.jobLocation == location)

        if skill:
            if skill not in ALLOWED_SKILLS:
                return jsonify({"error": f"Invalid skill. Choose from: {', '.join(ALLOWED_SKILLS)}"}), 400
            query = query.filter(Jobs.jobTitle.ilike(f"%{skill}%"))

        jobs = query.order_by(Jobs.postDate.desc()).all()

        jobs_data = [{
            "jobID": job.jobID,
            "employerID": job.employerID,
            "jobTitle": job.jobTitle,
            "jobLocation": job.jobLocation,
            "employmentType": job.employmentType,
            "postDate": job.postDate,
            "salaryRange": job.salaryRange
        } for job in jobs]

        return jsonify({"jobs": jobs_data}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to retrieve jobs"}), 500