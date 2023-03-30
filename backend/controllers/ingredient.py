import sys
sys.path.append("../")
from database.bootstrapDB import *
from flask_login import login_user
from flask import Blueprint, request

bp = Blueprint('ingredient', __name__)
ingredient_schema = IngredientSchema()
