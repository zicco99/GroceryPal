from flask_login import login_user
from flask import Blueprint, jsonify, request
from psycopg2 import IntegrityError
from database.DBootstrap import *
from controllers.user_contr import insert_db_if_misses

bp = Blueprint('feedback', __name__)
session = None

feedback_schema = FeedbackSchema()
feedbacks_schema = FeedbackSchema(many=True)



@bp.route('/', methods=['GET'])
def get_feedbacks():
    feedbacks = session.query(Feedback).all()
    return jsonify(feedbacks_schema(feedbacks))


@bp.route('/', methods=['POST'])
def create_feedback():
    data = request.json
    user_id = data.get('user_id')
    recipe_id = data.get('recipe_id')
    is_chosen = data.get('is_chosen')
    rating = data.get('rating')
    notes = data.get('notes')

    try:
        feedback = Feedback(user_id=user_id, recipe_id=recipe_id,
                            is_chosen=is_chosen, rating=rating, notes=notes)
        session.add(feedback)
        session.commit()
        return jsonify(feedback_schema.dump(feedback)), 201
    except IntegrityError:
        session.rollback()
        return jsonify({'message': 'User or Recipe does not exist'}), 400


@bp.route('/<int:feedback_id>', methods=['GET'])
def get_feedback_by_id(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if feedback:
        return jsonify(feedback_schema.dump(feedback))
    else:
        return jsonify({'message': 'Feedback not found'}), 404


@bp.route('/<int:id>', methods=['PUT'])
def update_feedback(id):
    feedback = Feedback.query.get(id)
    if feedback:
        data = request.json
        user_id = data.get('user_id')
        recipe_id = data.get('recipe_id')
        is_chosen = data.get('is_chosen')
        rating = data.get('rating')
        notes = data.get('notes')

        try:
            feedback.user_id = user_id
            feedback.recipe_id = recipe_id
            feedback.is_chosen = is_chosen
            feedback.rating = rating
            feedback.notes = notes

            session.commit()
            return jsonify(feedback_schema.dump(feedback))
        except IntegrityError:
            session.rollback()
            return jsonify({'message': 'User or Recipe does not exist'}), 400
    else:
        return jsonify({'message': 'Feedback not found'}), 404


@bp.route('/<int:id>', methods=['DELETE'])
def delete_feedback(id):
    feedback = Feedback.query.get(id)
    if feedback:
        session.delete(feedback)
        session.commit()
        return jsonify({'message': 'Feedback deleted'})
    else:
        return jsonify({'message': 'Feedback not found'}), 404


# TODO choose a better solution for both endpoints
@bp.route('/user-feedbacks/<int:user_id>', methods=['GET'])
def get_user_id_feedbacks(user_id):
    feedbacks = Feedback.query.filter_by(user_id=user_id).all()
    return jsonify(feedbacks_schema(feedbacks))


@bp.route('/recipe-feedbacks/<int:recipe_id>', methods=['GET'])
def get_recipe_feedbacks(recipe_id):
    feedbacks = Feedback.query.filter_by(recipe_id=recipe_id).all()
    return jsonify(feedbacks_schema(feedbacks))
