import sys
sys.path.append("../")
from database.bootstrapDB import *
from flask import Blueprint, request


bp = Blueprint('fridgeproduct', __name__)
fridgeproduct_schema = FridgeProductSchema()
