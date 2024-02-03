import sys
import os
from flask import Flask
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from model.studentModel import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'project2023' 
app.config['WTF_CSRF_ENABLED'] = False

@app.route('/api/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    return student(student_id)

@app.route('/api/showReward/<int:student_id>', methods=['GET'])
def get_tb_studentreward(student_id):
    return studentReward(student_id)

@app.route('/api/showItem', methods=['GET'])
def get_show():
    return showItem()

@app.route('/api/purchaseItem/<int:redeemitem_id>/<int:student_id>', methods=['POST'])
def item(redeemitem_id, student_id):
    return purchase(redeemitem_id, student_id)

@app.route('/api/showCoin/<int:student_id>', methods=['GET'])
def get_tb_studentcoin(student_id):
    return studentCoin(student_id)

@app.route('/api/enrollment', methods=['POST'])
def add_enrollment():
    return enrollmentPost()

@app.route('/api/enrollStatus', methods=['PUT'])
def get_enroll():
    return enrollPut()

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    return attendanceGet()

@app.route('/api/attendance', methods=['POST'])
def attendance():
    return attendanceAdd()

@app.route('/api/badge', methods=['PUT'])
def badgeUpdate():
    return badge()


#..(Other API routes)

if __name__ == '__main__':
    app.run(debug=True)