# controller/app.py
import sys
import os

from flask import Blueprint 
# Add the parent directory (project_root) to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from model.adminModel import *
#from validation.datavalidation import *
admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/student', methods=['GET'])
def get_student():
    return selectAllStudent()

@admin_blueprint.route('/register', methods=['POST'])
def student_reg():
    data = request.get_json()
    return registeration(data)
    
# Login
@admin_blueprint.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    return userlogin(data)

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

@admin_blueprint.route('/rewards',methods=['GET'])
def get_rewards():
    return getRewards()

@admin_blueprint.route('/rewards',methods=['POST'])
def add_reward():
    data = request.get_json()
    return addReward(data)

@admin_blueprint.route('/reward', methods=['DELETE'])
def delete_reward():
    reward_id = request.args.get("reward_id",type=int)
    db.commit()
    return deleteReward(reward_id)

@admin_blueprint.route('/item',methods=['GET'])
def get_redeemableitem():
    return getRedeemableitem()

@admin_blueprint.route('/item',methods=['POST'])
def add_redeemitem():
    data = request.get_json()
    return addRedeemitem(data)

@admin_blueprint.route('/item', methods=['DELETE'])
def delete_redeemableitem():
    item_id = request.args.get("item_id",type=int)
    return deleteRedeemableitem(item_id)

@admin_blueprint.route('/studentbadge', methods=['GET'])
def get_student_badges_api():
    student_id = request.args.get("student_id",type=int)
    badges = get_student_badges(student_id)
    return get_student_badges(student_id)

@admin_blueprint.route('/certificates', methods=['GET'])
def get_student_certificates_api():
    student_id = request.args.get("student_id",type=int)
    certificates = get_student_certificates(student_id)
    return get_student_certificates(student_id)

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


