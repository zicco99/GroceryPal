import sys
sys.path.append("../")
from database.bootstrapDB import *
from flask import Blueprint, jsonify, request


bp = Blueprint('fridgeproduct', __name__)

fridge_product_schema = FridgeProductSchema()
fridge_products_schema = FridgeProductSchema(many=True)

@bp.route('/fridge_products', methods=['GET'])
def get_fridge_products():
    fridge_products = FridgeProduct.query.all()
    return jsonify(fridge_products_schema.dump(fridge_products))


@bp.route('/fridge_products/<int:id>', methods=['GET'])
def get_fridge_product(id):
    fridge_product = FridgeProduct.query.get(id)
    if fridge_product:
        return jsonify(fridge_product_schema.dump(fridge_product))
    else:
        return jsonify({'message': 'Fridge product not found.'}), 404

@bp.route('/fridge_products', methods=['POST'])
def add_fridge_product():
    fridge_product = fridge_product_schema.load(request.json, session=session)
    existing_fridge_product = FridgeProduct.query.filter_by(fridge_id=fridge_product.fridge_id, product_id=fridge_product.product_id).first()
    
    if existing_fridge_product:
        existing_fridge_product.quantity += fridge_product.quantity
        session.commit()
        return jsonify(fridge_product_schema.dump(existing_fridge_product))

    session.add(fridge_product)
    session.commit()
    return jsonify(fridge_product_schema.dump(fridge_product)), 201


@bp.route('/fridge_products/<int:id>', methods=['DELETE'])
def delete_fridge_product(id):
    fridge_product = FridgeProduct.query.get(id)
    if fridge_product:
        session.delete(fridge_product)
        session.commit()
        return jsonify({'message': 'Fridge product deleted.'})
    else:
        return jsonify({'message': 'Fridge product not found.'}), 404
