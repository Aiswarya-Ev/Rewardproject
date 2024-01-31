import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from model.tutor import *

app = Flask(__name__)

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





if __name__ == '__main__':
    app.run(debug=True)