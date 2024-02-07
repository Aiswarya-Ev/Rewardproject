import sys
import os
from flask import Blueprint
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from model.tutor import *
tutor_blueprint = Blueprint('tutor', __name__)

@tutor_blueprint.route('/api/tutor', methods=['GET'])
def get_tutorView():
    return getTutorView()


@tutor_blueprint.route('/update', methods=['PUT'])
def update_tutor():
    tutor_id = request.args.get("tutor_id")
    return tutorPassword()


@tutor_blueprint.route("/tutorUpdation", methods=["PUT"])
def tutor_update():
    tutor_id = request.args.get("tutor_id")
    return tutorUpdation(tutor_id)


@tutor_blueprint.route('/std_assmnts', methods=['GET'])
def get_details():
    return tutview()    


@tutor_blueprint.route('/viewCourse', methods=['GET'])
def get_course():
    return viewcourse()

@tutor_blueprint.route('/addCourse', methods=['POST'])
def course_reg():
    return addcourse()

@tutor_blueprint.route('/courseDelete', methods=['DELETE'])
def delete_course():
    course_id = request.args.get("course_id",type=int)
    return deletecourse(course_id)

@tutor_blueprint.route('/assessmentView', methods=['GET'])
def get_assessment():
    return viewassessment()


@tutor_blueprint.route('/assessmentAdd', methods=['POST'])
def add_assessment():
    return addassessment()


@tutor_blueprint.route('/assessmentDelete', methods=['DELETE'])
def delete_assessment():
    as_id = request.args.get("as_id",type=int)
    return deleteassessment(as_id)


@tutor_blueprint.route('/completed_assessments', methods=['GET'])
def add_assessment_score():
    student_id = request.args.get("student_id",type=int)
    course_id = request.args.get("course_id",type=int)
    return assessmentCheck(student_id,course_id)


@tutor_blueprint.route('/select_courseId', methods=['GET'])
def select_courseId():
    as_id = request.args.get("as_id",type=int)
    courseid=selectcourseId(as_id)
    return jsonify({'course_id':courseid})

@tutor_blueprint.route('/update_password', methods=['PUT'])
def update_password():
    tutor_id = request.args.get("tutor_id",type=int)
    return tutor_password_update(tutor_id)