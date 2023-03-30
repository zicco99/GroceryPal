from flask import Blueprint, request
from database.bootstrapDB import *
import sys
sys.path.append("../")

bp = Blueprint('recipeingredient', __name__)
recipeingredient_schema = RecipeIngredientSchema()
