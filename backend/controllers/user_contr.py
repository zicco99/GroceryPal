from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from psycopg2 import IntegrityError
from database.bootstrapDB import *
import sys
sys.path.append("../")

bp = Blueprint('user', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@bp.route('/users', methods=['GET'])
def get_users():
    users = session.query(User).all()
    return users_schema.jsonify(users)


@bp.route('/users', methods=['POST'])
def create_user():
    try:
        user = user_schema.load(request.json, session=session)
        session.add(user)
        session.commit()
        return user_schema.jsonify(user)
    except ValidationError as e:
        session.rollback()
        return jsonify({'error': e.messages}), 400
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'User already exists.'}), 409


@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = session.query(User).get(user_id)
    if user:
        return user_schema.jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404


@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        user = user_schema.load(
            request.json, session=session, instance=user, partial=True)
        session.commit()
        return user_schema.jsonify(user)
    except ValidationError as e:
        session.rollback()
        return jsonify({'error': e.messages}), 400
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'User already exists.'}), 409


@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404
    

def insert_db_if_misses(user):
    if not session.query(User).filter_by(id=user.id).first():
        session.add(user)
        session.commit()


def get_user(user_id):
    return session.query(User).filter_by(id=user_id).first()
