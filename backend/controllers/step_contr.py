from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from psycopg2 import IntegrityError
from database.bootstrapDB import *
import sys
sys.path.append("../")

bp = Blueprint('step', __name__)
step_schema = StepSchema()
steps_schema = StepSchema(many=True)


@bp.route('/', methods=['GET'])
def list_steps():
    steps = Step.query.all()
    return steps_schema.jsonify(steps)


@bp.route('/', methods=['POST'])
def create_step():
    try:
        step = step_schema.load(request.json, session= session)
        session.add(step)
        session.commit()
        return step_schema.jsonify(step)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'Integrity error'}), 409


@bp.route('/<int:step_id>', methods=['GET'])
def get_step(step_id):
    step = Step.query.get(step_id)
    if not step:
        return jsonify({'error': 'Step not found'}), 404
    return step_schema.jsonify(step)


@bp.route('/<int:step_id>', methods=['PUT'])
def update_step(step_id):
    try:
        step = Step.query.get(step_id)
        if not step:
            return jsonify({'error': 'Step not found'}), 404
        step = step_schema.load(request.json, instance=step, session=session)
        session.commit()
        return step_schema.jsonify(step)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'Integrity error'}), 409


@bp.route('/<int:step_id>', methods=['DELETE'])
def delete_step(step_id):
    step = Step.query.get(step_id)
    if not step:
        return jsonify({'error': 'Step not found'}), 404
    session.delete(step)
    session.commit()
    return jsonify({'message': 'Step deleted successfully'})


