from flask import Blueprint, request, jsonify
from flask_login import login_user
from flask import Blueprint, jsonify, request
from database.DBootstrap import *


bp = Blueprint('fridge', __name__)

fridge_schema = FridgeSchema()
fridges_schema = FridgeSchema(many=True)

@bp.route('/fridges', methods=['POST'])
def create_fridge():
    name = request.json.get('name')
    if not name:
        return jsonify({'message': 'Name is required'}), 400
    fridge = Fridge(name=name)
    session.add(fridge)
    session.commit()
    return jsonify(fridge_schema.dump(fridge)), 201


@bp.route('/fridges/<int:id>', methods=['PUT'])
def update_fridge(id):
    fridge = Fridge.query.get(id)
    if not fridge:
        return jsonify({'message': 'Fridge not found'}), 404
    name = request.json.get('name')
    if not name:
        return jsonify({'message': 'Name is required'}), 400
    fridge.name = name
    session.commit()
    return jsonify(fridge_schema.dump(fridge)), 200


@bp.route('/fridges/<int:id>', methods=['DELETE'])
def delete_fridge(id):
    fridge = Fridge.query.get(id)
    if not fridge:
        return jsonify({'message': 'Fridge not found'}), 404
    session.delete(fridge)
    session.commit()
    return '', 204


@bp.route('/fridges', methods=['GET'])
def list_fridges():
    all_fridges = Fridge.query.all()
    result = fridges_schema.dump(all_fridges)
    return jsonify(result)


@bp.route('/fridges/<int:id>', methods=['GET'])
def get_fridge_by_id(id):
    fridge = Fridge.query.get(id)
    if not fridge:
        return jsonify({'message': 'Fridge not found'}), 404
    return jsonify(fridge_schema.dump(fridge))
