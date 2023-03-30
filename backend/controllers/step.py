from flask import Blueprint, request
from database.bootstrapDB import *
import sys
sys.path.append("../")

bp = Blueprint('step', __name__)
step_schema = StepSchema()
