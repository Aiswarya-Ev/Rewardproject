# controller/app.py
import sys
import os

from flask import Blueprint 
# Add the parent directory (project_root) to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from model.adminModel import *
#from validation.datavalidation import *
api_blueprint= Blueprint('api', __name__)

@api_blueprint.route('/register', methods=['POST'])
def student_reg():
    data = request.get_json()
    return registeration(data)
    
# Login
@api_blueprint.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    return userlogin(data)
@api_blueprint.route('/count', methods=['GET'])
def count_tutor():
    return get_tutors_count()