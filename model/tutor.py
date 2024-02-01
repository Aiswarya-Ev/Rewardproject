import mysql.connector #connect sql
from flask import Flask, jsonify, request #convert Python dictionaries to JSON format 
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from configuration import mysql_config
import bcrypt
from flask_bcrypt import check_password_hash
from flask_bcrypt import generate_password_hash

db = mysql.connector.connect(**mysql_config)
cursor = db.cursor()


def getTutorView():
    try:
        cursor.execute('SELECT * FROM tb_tutor')
        tutor = cursor.fetchall()
        return jsonify({'tb_tutor': tutor})
    except Exception as e:
        return jsonify({'error': str(e)})
    
def tutorGet(tutor_id):
    try:
        cursor.execute('SELECT login_id FROM tb_tutor WHERE tutor_id=%s',(tutor_id,))
        tutor = cursor.fetchone()
        return jsonify({'tb_tutor': tutor})
    except Exception as e:
        return jsonify({'error': str(e)})

def tutorPassword(login_id):
    try:
        data = request.get_json()
        new_password = data.get('new_password')
        
        if new_password:
            hashed_password = generate_password_hash(new_password).decode('utf-8')
            cursor.execute('UPDATE tb_login SET userpassword = %s WHERE login_id = %s', (hashed_password, login_id))
            db.commit()
        return jsonify({'message': 'Update successful'})
    except Exception as e:
        return jsonify({'error': str(e)})


def tutorUpdation(tutor_id):
    try:
        cursor.execute('SELECT * FROM tb_tutor WHERE tutor_id = %s', (tutor_id,))
        tutor = cursor.fetchone()

        if tutor is None:
            return jsonify({'message': 'tutor not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided in the request'}), 400

        # Update only the fields provided in the JSON payload
        updated_fields = []
        for key, value in data.items():
                cursor.execute(f'UPDATE tb_tutor SET {key} = %s WHERE tutor_id = %s', (value, tutor_id))
                updated_fields.append(key)

        db.commit()

        return jsonify({'message': 'tutor data updated successfully', 'updated_fields': updated_fields})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def tutview():
    try:
        cursor.execute('SELECT s_name, as_name, as_date FROM tb_student s JOIN tb_assessment a ON s.student_id = a.student_id;')
        res = cursor.fetchall()
        return jsonify(res)
    except Exception as e:
        return jsonify({'error': str(e)})
    

def viewcourse():
    try:
        cursor.execute('SELECT * FROM tb_course')
        course = cursor.fetchall()
        return jsonify({'tb_course': course})
    except Exception as e:
        return jsonify({'error': str(e)})

def addcourse():
    try:
        data = request.get_json()
        name = data.get('c_name')
        start_date = data.get('start_date')
        coins = data.get('coins')
        assessment_no = data.get('assessment_no')
        tutor_id = data.get('tutor_id')

        cursor.execute('INSERT INTO tb_course (c_name, start_date, coins, assessment_no, tutor_id) VALUES (%s, %s, %s, %s, %s)', (name, start_date, coins, assessment_no, tutor_id))
        db.commit()
        return jsonify({'message': 'Course entered successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
def deletecourse(course_id):
    try:
        cursor.execute('SELECT * FROM tb_course WHERE course_id = %s', (course_id,))
        
        # Fetch the result set
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'error': 'Course not found with the given ID'}), 404

        # Delete the course if it exists
        cursor.execute('DELETE FROM tb_course WHERE course_id = %s', (course_id,))
        db.commit()

        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def viewassessment():
    try:
        cursor.execute('SELECT * FROM tb_assessment')
        assessment = cursor.fetchall()
        return jsonify({'tb_assessment': assessment})
    except Exception as e:
        return jsonify({'error': str(e)})
    

def addassessment():
    try:
        data = request.get_json()
        name = data.get('as_name')
        as_date = data.get('as_date')
        courseid = data.get('course_id')

        cursor.execute('INSERT INTO tb_assessment (as_name, as_date, course_id) VALUES (%s, %s, %s)', (name, as_date, courseid))
        db.commit()
        return jsonify({'message': 'Entered successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
     

def deleteassessment(as_id): 
    try:
        cursor.execute('SELECT * FROM tb_assessment WHERE as_id = %s', (as_id,))
        
        # Fetch the result set
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'error': 'Assessment not found with the given ID'}), 404

        # Delete the course if it exists
        cursor.execute('DELETE FROM tb_assessment WHERE as_id = %s', (as_id,))
        db.commit()

        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def assessmentCheck(student_id,course_id):
    try:
        # Fetch the total assessment number required for the course
        cursor.execute('SELECT assessment_no FROM tb_course WHERE course_id IN (SELECT course_id FROM tb_enrollment WHERE student_id = %s)', (student_id,))
        total_assessmentNo=cursor.fetchone()
        cursor.execute('SELECT COUNT(*) as count FROM tb_attendance ad JOIN tb_assessment at ON ad.assessment_id = at.as_id WHERE ad.student_id = %s AND at.course_id = %s', (student_id, course_id))
        completed_assessmentsCount = cursor.fetchone()[0]

        if completed_assessmentsCount <= total_assessmentNo[0]:
            return jsonify({'message': 'Student has already completed all assessments and cannot add more.'})

        return jsonify({'message': 'Assessment completed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})