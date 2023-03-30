from flask import Blueprint, request
from database.bootstrapDB import *
import sys
sys.path.append("../")

bp = Blueprint('userfridge', __name__)
userfrdige_schema = UserFridgeSchema()
