from flask_login import login_user
from flask import Blueprint, jsonify, request
from database.bootstrapDB import *
import sys
from backend.controllers.user import insert_db_if_misses
sys.path.append("../")


bp = Blueprint('fridge', __name__)
fridge_schema = FridgeSchema()


@bp.route("/list-fridges", methods=['GET'])
def list_fridges():
    user = User(id=100000, name="vai mo",
                email="tina cipollari", profile_pic="www.goo")

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)

    if request.method == 'GET':
        return listFridges(user.id)


@bp.route("/new-fridge", methods=['POST'])
def new_fridge():

    user = User(id=100000, name="vai mo",
                email="tina cipollari", profile_pic="www.goo")

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)

    if request.method == 'POST':
        return newFridge(user_id=user.id, fridge_name=request.json)


# Endpoints controller
fridge_schema = FridgeSchema()


def listFridges(user_id):
    user_fridges = session.query(UserFridge).filter(
        UserFridge.user_id == user_id).all()

    fridges_json = []
    for uf in user_fridges:
        fridge = session.query(Fridge).get(uf.fridge_id)
        fridges_json.append(fridge_schema.dump(fridge))

    # Return the list of recipe dictionaries in a JSON response
    return jsonify(fridges_json)


def newFridge(user_id, fridge_name):

    user = session.query(User).get(user_id)
    existing_fridge = session.query(Fridge).filter_by(name=fridge_name).first()

    if existing_fridge:
        raise ValueError(
            f"A fridge with the name '{fridge_name}' already exists.")

    new_fridge = Fridge(name=fridge_name)
    user.fridges.append(new_fridge)
    new_user_fridge = UserFridge(
        user_id=user.id, fridge_id=new_fridge.id, is_admin=True, is_owner=True)

    session.add(new_fridge)
    session.add(new_user_fridge)
    session.commit()

    serialized_fridge = fridge_schema.dump(new_fridge)
    return jsonify(serialized_fridge)
