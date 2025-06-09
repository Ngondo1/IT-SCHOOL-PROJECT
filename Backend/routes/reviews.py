from flask import Blueprint, request, jsonify
from models import db, Ratings, Users
from datetime import datetime

review_bp = Blueprint('review_bp', __name__, url_prefix='/api/reviews')

ALLOWED_RATING_VALUES = [1, 2, 3, 4, 5]

@review_bp.route('/submit', methods=['POST'])
def submit_review():
    data = request.get_json()
    required_fields = ['raterID', 'rateeID', 'rating', 'comment']

    for field in required_fields:
        if field not in data or str(data[field]).strip() == '':
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    if data['raterID'] == data['rateeID']:
        return jsonify({"error": "You cannot rate yourself."}), 400

    if int(data['rating']) not in ALLOWED_RATING_VALUES:
        return jsonify({"error": "Rating must be an integer between 1 and 5."}), 400

    existing_review = Ratings.query.filter_by(
        raterID=data['raterID'], rateeID=data['rateeID']
    ).first()

    if existing_review:
        return jsonify({"error": "You have already rated this user."}), 409

    rater = Users.query.filter_by(userID=data['raterID']).first()
    ratee = Users.query.filter_by(userID=data['rateeID']).first()

    if not rater or not ratee:
        return jsonify({"error": "One or both users not found."}), 404

    new_rating = Ratings(
        raterID=data['raterID'],
        rateeID=data['rateeID'],
        rating=int(data['rating']),
        comment=data['comment'].strip(),
        timestamp=datetime.utcnow()
    )

    try:
        db.session.add(new_rating)
        db.session.commit()
        return jsonify({"message": "Review submitted successfully!"}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@review_bp.route('/get_by_user/<int:user_id>', methods=['GET'])
def get_reviews_for_user(user_id):
    reviews = Ratings.query.filter_by(rateeID=user_id).order_by(Ratings.timestamp.desc()).all()

    reviews_data = [{
        "rating": r.rating,
        "comment": r.comment,
        "timestamp": r.timestamp
    } for r in reviews]

    return jsonify({"reviews": reviews_data}), 200