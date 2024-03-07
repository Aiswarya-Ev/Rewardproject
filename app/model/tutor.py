import mysql.connector #connect sql
from flask import Flask, jsonify, request #convert Python dictionaries to JSON format 
import sys
import os 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from validation.Validate import *
from model.featureModel import checkAssessmentCompletion 
from configuration.config import mysql_config
import bcrypt
from flask_bcrypt import check_password_hash
from flask_bcrypt import generate_password_hash
from utilities.utilities import*

db = mysql.connector.connect(**mysql_config)
cursor = db.cursor()

def select_tutor_details(tablename,fieldname,student_id):
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
        cursor.execute(f'SELECT  * FROM {tablename}  WHERE {fieldname} = %s',(student_id,))
        data = cursor.fetchall()
        structured_items = []
        structured_items.append({
        'id': data[0][0],
        'username': data[0][1],
        'date': data[0][2],
          'email': data[0][3],
        'phone': data[0][4],
        'house_no': data[0][7],
          'city': data[0][8],
        'state': data[0][9],
        'country': data[0][10],
          'pin': data[0][11],
        'login': data[0][5]  # Assuming third column is description
        })
        return generate_response(structured_items)
    except Exception as e:
        return jsonify({'Error':str(e)}) 
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()
def getTutorView():
    try:
        cursor.execute('SELECT * FROM tb_tutor')
        tutor = cursor.fetchall()
        return jsonify({'tb_tutor': tutor})
    except Exception as e:
        return jsonify({'error': str(e)})
    

def tutorPassword(tutor_id):
    try:
        # Check if tutor_id exists
        cursor.execute('SELECT login_id FROM tb_tutor WHERE tutor_id = %s', (tutor_id,))
        tutor = cursor.fetchone()

        if tutor is None:
            return jsonify({'error': 'Tutor not found'})

        tutor_login_id = tutor[0]  # Extract the login_id from the tuple

        data = request.get_json()
        new_password = data.get('new_password')

        if new_password:
            hashed_password = generate_password_hash(new_password)
            cursor.execute('UPDATE tb_login SET userpassword = %s WHERE login_id = %s', (hashed_password, tutor_login_id))
            is_valid, error_message = validate_password(data)
            if not is_valid:
                return jsonify({'error': error_message})
            db.commit()
            return jsonify({'message': 'Password updated successfully'})

        return jsonify({'error': 'Password is required'})

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

        is_valid, error_message = validate_tutor(data)
        if not is_valid:
            return jsonify({'error': error_message})
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
    

def viewcourse(tutor_id):
    try:
        cursor.execute('SELECT * FROM tb_course where tutor_id=%s',(tutor_id,))
        course = cursor.fetchall()
        structured_items=[]
        for data in course:
            structured_items.append({
            'course_id': data[0],
            'c_name': data[1],
            'start_date': data[2],
            'coins': data[3],
            'tutor_id': data[4],
            'assessment_no': data[5]
        })
        return generate_response(structured_items)
    except Exception as e:
        return jsonify({'error': str(e)})

def addcourse():
    try:
        data = request.get_json()
        name = data.get('c_name')
        start_date = data.get('start_date')
        coins = data.get('coins')
        tutor_id = data.get('tutor_id')
        cursor.execute('INSERT INTO tb_course (c_name, start_date, coins,tutor_id) VALUES (%s, %s, %s,%s)', (name, start_date, coins,tutor_id))
        db.commit()
        is_valid, error_message = validate_course(data)
        if not is_valid:
            return jsonify({'error': error_message})
        return jsonify({'message': 'Course entered successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
def deletecourse(course_id):
    try:
        cursor.execute('SELECT * FROM tb_course WHERE course_id = %s', (course_id,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'error': 'Course not found with the given ID'}), 404
        cursor.execute('DELETE FROM tb_course WHERE course_id = %s', (course_id,))
        db.commit()
        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def viewassessment(tutor_id):
    try:
        cursor.execute('''SELECT ta.*
        FROM tb_assessment ta
        JOIN tb_course tc ON ta.course_id = tc.course_id
        WHERE tc.tutor_id = %s''',(tutor_id,))
        assessment = cursor.fetchall()
        structured_items=[]
        for data in assessment:
            structured_items.append({
            'assessment_id': data[0],
            'as_name': data[1],
            'as_date': data[2],
            'course_id': data[3],
            'coins': data[4],
            'total':data[5]
        })
        return generate_response(structured_items)
    except Exception as e:
        return jsonify({'error': str(e)})
    

def addassessment():
    try:
        data = request.get_json()
        name = data.get('as_name')
        as_date = data.get('as_date')
        course_id = data.get('course_id')
        coins=data.get('coins')
        cursor.execute('INSERT INTO tb_assessment (as_name, as_date, course_id,coins) VALUES (%s, %s, %s,%s)', (name, as_date, course_id,coins))
        db.commit()
        cursor.execute('select assessment_no from tb_course where course_id=%s',(course_id,))
        number=cursor.fetchone()[0]
        number=number+1
        cursor.execute('update tb_course set assessment_no=%s where course_id=%s',(number,course_id))
        is_valid, error_message = validate_assessment(data)
        if not is_valid:
            return jsonify({'error': error_message})
        db.commit()
        return jsonify({'message': 'Entered successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
     

def deleteassessment(as_id): 
    try:
        cursor.execute('SELECT course_id FROM tb_assessment WHERE as_id = %s', (as_id,))
        
        # Fetch the result set
        result = cursor.fetchone()[0]
        
        if not result:
            return jsonify({'error': 'Assessment not found with the given ID'}), 404

        # Delete the course if it exists
        cursor.execute('select assessment_no from tb_course where course_id=%s',(result,))
        number=cursor.fetchone()[0]
        number=number-1
        cursor.execute('update tb_course set assessment_no=%s where course_id=%s',(number,result))
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
    

def selectcourseId(as_id):
    try:
        cursor.execute('SELECT course_id FROM tb_assessment WHERE as_id = %s', (as_id,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None 
    except Exception as e:
        print(f"Error: {e}")

def tutor_password_update(tutor_id):
    try:
        # Fetch the tutor's current hashed password from the database
        cursor.execute('SELECT userpassword FROM tb_login WHERE login_id = %s', (tutor_id,))
        current_password_hash = cursor.fetchone()[0]
 
        # Get the old password and the new password from the request data
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
 
        # Check if the old password matches the stored hashed password
        if check_password_hash(current_password_hash, old_password):
            # Hash the new password and update it in the database
            hashed_password = generate_password_hash(new_password)
            cursor.execute('UPDATE tb_login SET userpassword = %s WHERE login_id = %s', (hashed_password, tutor_id))
            db.commit()
            return jsonify({'message': 'Password updated successfully'})
        else:
            return jsonify({'error': 'Old password is incorrect'}), 401
 
    except Exception as e:
        return jsonify({'error': str(e)}), 500