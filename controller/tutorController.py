import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from model.tutor import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex2023' 
app.config['WTF_CSRF_ENABLED'] = False

@app.route('/api/tutor', methods=['GET'])
def get_tutorView():
    return getTutorView()

@app.route('/api/retreiveId/<int:tutor_id>', methods=['GET'])
def get_tutor(tutor_id):
    return tutorGet(tutor_id)

@app.route('/api/tutor/update/<int:login_id>', methods=['PUT'])
def update_tutor(login_id):
    return tutorPassword(login_id)


@app.route("/api/tutorUpdation/<int:tutor_id>", methods=["PUT"])
def tutor_update(tutor_id):
    return tutorUpdation(tutor_id)


@app.route('/api/tutor/std_assmnts', methods=['GET'])
def get_details():
    return tutview()    


@app.route('/api/viewCourse', methods=['GET'])
def get_course():
    return viewcourse()

@app.route('/api/addCourse', methods=['POST'])
def course_reg():
    return addcourse()

@app.route('/api/courseDelete/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    return deletecourse(course_id)

@app.route('/api/assessmentView', methods=['GET'])
def get_assessment():
    return viewassessment()


@app.route('/api/assessmentAdd', methods=['POST'])
def add_assessment():
    return addassessment()


@app.route('/api/assessmentDelete/<int:as_id>', methods=['DELETE'])
def delete_assessment(as_id):
    return deleteassessment(as_id)


@app.route('/api/student/completed_assessments/<int:student_id>,<int:course_id>', methods=['GET'])
def add_assessment_score(student_id,course_id):
    return assessmentCheck(student_id,course_id)



if __name__ == '__main__':
    app.run(debug=True)