from flask import Blueprint, request, jsonify
from models import db, MatchesRequest, Users
from datetime import datetime

match_bp = Blueprint('match_bp', __name__, url_prefix='/api/matches')

@match_bp.route('/request', methods=['POST'])
def request_match():
    data = request.get_json()
    required_fields = ['requester_phoneNo', 'match_phoneNo']

    for field in required_fields:
        if field not in data or not data[field].strip():
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    requester = Users.query.filter_by(phoneNo=data['requester_phoneNo']).first()
    match_target = Users.query.filter_by(phoneNo=data['match_phoneNo']).first()

    if not requester or not match_target:
        return jsonify({"error": "Both users must exist in the system."}), 404

    existing = MatchesRequest.query.filter_by(
        requester_phoneNo=data['requester_phoneNo'],
        match_phoneNo=data['match_phoneNo']
    ).first()

    if existing:
        return jsonify({"error": "Match request already exists."}), 409

    match_request = MatchesRequest(
        requester_phoneNo=data['requester_phoneNo'],
        match_phoneNo=data['match_phoneNo'],
        request_time=datetime.utcnow(),
        status='pending'
    )

    try:
        db.session.add(match_request)
        db.session.commit()
        return jsonify({"message": "Match request submitted successfully.", "matchID": match_request.matchID}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@match_bp.route('/update_status', methods=['POST'])
def update_match_status():
    data = request.get_json()
    required_fields = ['matchID', 'status']

    if data['status'] not in ['approved', 'declined']:
        return jsonify({"error": "Invalid status value. Use 'approved' or 'declined'."}), 400

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    match = MatchesRequest.query.get(data['matchID'])

    if not match:
        return jsonify({"error": "Match request not found."}), 404

    match.status = data['status']

    try:
        db.session.commit()
        return jsonify({"message": f"Match status updated to '{data['status']}'"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@match_bp.route('/get_by_phone', methods=['GET'])
def get_matches_by_phone():
    phoneNo = request.args.get('phoneNo')

    if not phoneNo:
        return jsonify({"error": "Missing phone number"}), 400

    matches = MatchesRequest.query.filter_by(requester_phoneNo=phoneNo).all()

    data = [{
        "matchID": m.matchID,
        "match_phoneNo": m.match_phoneNo,
        "status": m.status,
        "request_time": m.request_time
    } for m in matches]

    return jsonify({"match_requests": data}), 200
