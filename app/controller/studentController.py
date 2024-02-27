import sys
from flask import Blueprint,session
import os
from flask import Flask
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
student_blueprint = Blueprint('student', __name__)
from model.studentModel import *
from model.featureModel import *
@student_blueprint.route('/', methods=['GET'])
def get_student_info():
    login_id = request.args.get("login_id",type=int)
    return select_student_details("tb_student","login_id",login_id)
@student_blueprint.route('/course', methods=['GET'])
def get_course():
    student_id = request.args.get("student_id",type=int)
    return getCourse(student_id)
@student_blueprint.route('/order', methods=['GET'])
def get_order():
    student_id = request.args.get("student_id",type=int)
    return get_items_by_student_id(student_id)
@student_blueprint.route('/details', methods=['GET'])
def get_Details():
    student_id = request.args.get("student_id",type=int)
    return get_details(student_id)
    #return select_student_details("tb_student","student_id",student_id)
@student_blueprint.route('/student', methods=['PUT'])
def update_student():
    student_id = request.args.get("student_id",type=int)
    return student(student_id)
@student_blueprint.route('/oldcourses', methods=['GET'])
def get_student_courses_api():
    student_id = request.args.get("student_id",type=int)
    return get_student_certificates(student_id)
@student_blueprint.route('/unentrolled', methods=['GET'])
def get_student_untrolled():
    student_id = request.args.get("student_id",type=int)
    return get_unenrolled_courses(student_id)
@student_blueprint.route('/ongoing', methods=['GET'])
def get_student_ongoing():
    student_id = request.args.get("student_id",type=int)
    return getCourse(student_id)
@student_blueprint.route('/assssment', methods=['GET'])
def get_student_assessment():
    student_id = request.args.get("student_id",type=int)
    course_id= request.args.get("course_id",type=int)
    return getAssessment(course_id,student_id)

# @student_blueprint.route('/showReward', methods=['GET'])
# def get_tb_studentreward():
#     student_id = request.args.get("student_id",type=int)
#     return studentReward(student_id)

@student_blueprint.route('showItem', methods=['GET'])
def get_show():
    student_id = request.args.get("student_id",type=int)
    items = get_items_by_student_id(student_id)
    if items:
        return generate_response(items)
    else:
        return generate_response(status_code=404)

@student_blueprint.route('/purchaseItem', methods=['POST'])
def item():
    item_id = request.args.get("item_id")
    student_id = request.args.get("student_id",type=int)
    return purchase(item_id, student_id)
@student_blueprint.route('/purchaseItem', methods=['GET'])
def getitem():
    return getPurchaseitem()

# @student_blueprint.route('/showCoin', methods=['GET'])
# def get_tb_studentcoin():
#     student_id = request.args.get("student_id",type=int)
#     return studentCoin(student_id)

@student_blueprint.route('/enrollment', methods=['POST'])
def add_enrollment():
    course_id = request.args.get("course_id",type=int)
    student_id = request.args.get("student_id",type=int)
    return enrollmentPost(course_id,student_id)

@student_blueprint.route('/score', methods=['POST'])
def add_score():
    try:
        student_id=request.args.get("student_id",type=int)
        as_id=request.args.get("as_id",type=int)
        score= request.args.get("score",type=int)
        if score is None or not (0 <= score<= 10):
            return jsonify({"error": "Invalid score (must be an integer between 0 and 10)"}), 400
        #if score[0]>10 or score[0]<0:
           # return jsonify({'messege':'score should be less than 10 and greater then 0'})
        return certification(student_id,as_id,score)
    except Exception as e:
        return jsonify({'Error':str(e)})

# @student_blueprint.route('/certi',methods=['POST'])
# def check(student_id,as_id):
#     return certificate(student_id,as_id)

# @student_blueprint.route('/enrollStatus', methods=['PUT'])
# def get_enroll():
#     return enrollPut()

# @student_blueprint.route('/attendance', methods=['GET'])
# def get_attendance():
#     return attendanceGet()

# @student_blueprint.route('/attendance', methods=['POST'])
# def attendance():
#     return attendanceAdd()

# @student_blueprint.route('/badge', methods=['PUT'])
# def badgeUpdate():
#     return badge()


