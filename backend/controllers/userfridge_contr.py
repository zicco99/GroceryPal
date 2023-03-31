from flask import Blueprint, jsonify, request
from database.bootstrapDB import *
import sys
sys.path.append("../")

bp = Blueprint('userfridge', __name__)
userfridge_schema = UserFridgeSchema()


@bp.route('/user_fridges', methods=['POST'])
def add_user_fridge():
    # Load UserFridge object from request data
    user_fridge = userfridge_schema.load(request.json, session=session)

    # Add UserFridge to database and commit session
    session.add(user_fridge)
    session.commit()

    # Return serialized UserFridge object as response
    return userfridge_schema.dump(user_fridge), 201


@bp.route('/user_fridges/<int:user_fridge_id>', methods=['PUT'])
def update_user_fridge(user_fridge_id):
    # Query for UserFridge object by id
    user_fridge = UserFridge.query.get(user_fridge_id)
    if not user_fridge:
        return jsonify({'error': 'UserFridge not found'}), 404

    # Update UserFridge object with request data
    user_fridge = userfridge_schema.load(
        request.json, instance=user_fridge, session=session)

    # Commit session
    session.commit()

    # Return serialized UserFridge object as response
    return userfridge_schema.dump(user_fridge), 200


@bp.route('/user_fridges/<int:user_fridge_id>', methods=['DELETE'])
def delete_user_fridge(user_fridge_id):
    # Query for UserFridge object by id
    user_fridge = UserFridge.query.get(user_fridge_id)
    if not user_fridge:
        return jsonify({'error': 'UserFridge not found'}), 404

    # Remove UserFridge from database and commit session
    session.delete(user_fridge)
    session.commit()

    # Return success message as response
    return jsonify({'message': 'UserFridge deleted successfully'}), 200
