from flask_login import login_user
from flask import Blueprint, request
from database.bootstrapDB import *
import sys
from backend.controllers.user import insert_db_if_misses
sys.path.append("../")

bp = Blueprint('feedback', __name__)
feedback_schema = FeedbackSchema()


@bp.route("/add-feedback", methods=['GET'])
def list_fridges(user_id, is_chosen, recipe_id):

    user = User(id=100000, name="vai mo",
                email="tina cipollari", profile_pic="www.goo")

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)

    if request.method == 'GET':
        try:
            user = session.query(User).get(user_id)
            recipe = session.query(Recipe).get(recipe_id)
            if not user or not recipe:
                return None

            existingFeeback = session.query(Feedback).filter(
                Feedback.user_id == user_id, Feedback.recipe_id == recipe_id).first()
            if not existingFeeback:
                new_feeback = Feedback(
                    user_id=user_id, recipe_id=recipe_id, is_chosen=is_chosen)
                session.add(new_feeback)
                session.commit()
                return 1

        except Exception as e:
            session.rollback()
            print(e)
            return None
