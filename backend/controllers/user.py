from flask import Blueprint, request
from database.bootstrapDB import *
import sys
sys.path.append("../")

bp = Blueprint('user', __name__)
user_schema = UserSchema()

def insert_db_if_misses(user):
    if not session.query(User).filter_by(id=user.id).first():
        session.add(user)
        session.commit()


def get_user(user_id):
    return session.query(User).filter_by(id=user_id).first()
