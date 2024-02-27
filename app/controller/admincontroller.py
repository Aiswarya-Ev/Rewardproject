# controller/app.py
import sys
import os

from flask import Blueprint 
# Add the parent directory (project_root) to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from model.adminModel import *
#from validation.datavalidation import *
admin_blueprint = Blueprint('admin', __name__)


# @admin_blueprint.route('/student', methods=['GET'])
# def get_student():
#     return selectAllStudent()
@admin_blueprint.route('/', methods=['GET'])
def get_admin():
    login_id = request.args.get("login_id",type=int)
    return selectAdmin(login_id)

@admin_blueprint.route('/tutor', methods=['GET'])
def get_tutor():
    return viewTutor()
@admin_blueprint.route('/tutor', methods=['DELETE'])
def delete_tutor():
    tutor_id = request.args.get("tutor_id",type=int)
    return deleteTutor(tutor_id)

@admin_blueprint.route('/tutor', methods=['PUT'])
def update_item():
    tutor_id = request.args.get("tutor_id",type=int)
    return approve(tutor_id)

@admin_blueprint.route('/item',methods=['GET'])
def get_redeemableitem():
    return getRedeemableitem()
@admin_blueprint.route('/course',methods=['GET'])
def get_courses():
    return getCourse()

@admin_blueprint.route('/item',methods=['POST'])
def add_redeemitem():
    data = request.get_json()
    return addRedeemitem(data)

@admin_blueprint.route('/item', methods=['DELETE'])
def delete_redeemableitem():
    item_id = request.args.get("item_id",type=int)
    return deleteRedeemableitem(item_id)

@admin_blueprint.route('/search', methods=['GET'])
def search_items_api():
    item_name = request.args.get('name', '')  # Get the 'name' parameter from the query string

    if not item_name:
        return jsonify({'message': 'Please provide a valid item name'}), 400

    return search_items_by_name(item_name)

    # if items is not None:
    #     return jsonify({'items': items})
    # else:
    #     return jsonify({'message': 'Error searching for items'}), 500
    
@admin_blueprint.route('/oldcourses', methods=['GET'])
def get_student_courses_api():
    student_id = request.args.get("student_id",type=int)
    return get_student_courses(student_id)
# ... (other API routes)


