# model/program
import bcrypt
from flask import Flask, jsonify, request
from flask_bcrypt import check_password_hash
import sys
import os
# Add the parent directory (project_root) to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from configuration.config import db
from validation.validation import *
cursor = db.cursor()


def selectAllStudent():
    try:
        cursor.execute('SELECT * FROM tb_student')
        student =cursor.fetchall()
        return jsonify({'tb_student': student})
    except Exception as e:
        return jsonify({'Error':str(e)})
def registeration(data):
    try:
        name = data.get('s_name')
        dob = data.get('s_dob')
        email = data.get('s_email')
        phone = data.get('s_phoneno')
        house = data.get('s_houseno')
        city = data.get('s_city')
        state = data.get('s_state')
        country = data.get('s_country')  # Corrected variable name
        pin = data.get('s_pin')
        username = data.get('username')
        password = data.get('userpassword')
        user_type = data.get('type')  # Corrected variable name

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        is_valid, error_message = validate_signup_data(data)
        if not is_valid:
            return jsonify({'error': error_message})
        else:
            # Insert login details into 'login' table
            cursor.execute('INSERT INTO tb_login (username, userpassword, type) VALUES (%s, %s, %s)',
                        (username, hashed_password, user_type))
            login_id = cursor.lastrowid
            if user_type=='student':
            # Insert student details into 'students' table
                cursor.execute('INSERT INTO tb_student (s_name, s_dob, s_email, s_phoneno, s_houseno, s_city, s_state, s_country, s_pin, login_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (name, dob, email, phone, house, city, state, country, pin, login_id))
                s_id = cursor.lastrowid
                cursor.execute('INSERT INTO tb_supercoin (student_id) VALUES (%s)', (s_id,))
            else:
                cursor.execute('INSERT INTO tb_tutor(t_name, t_dob, t_email, t_phoneno, t_houseno, t_city, t_state, t_country, t_pin, login_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (name, dob, email, phone, house, city, state, country, pin, login_id))
            db.commit()
            return jsonify({'message': 'Registration successful'})
    except Exception as e:
        return jsonify({'Error':str(e)})

def userlogin(data):
    try:
        username = data.get('username')
        user_password = data.get('userpassword')  # Corrected variable name
        is_valid,error_message = username_password(data)
        if not is_valid:
            return jsonify({'error': error_message})
        else:
            cursor.execute('SELECT * FROM tb_login WHERE username = %s', (username,))
            results = cursor.fetchone()

            if results:
                hashed_password = results[2]
                if hashed_password and check_password_hash(hashed_password, user_password):
                    user_type = results[3]
                    if user_type in ['admin', 'student']:
                        return jsonify({'message': f'{user_type} login successfully'})
                    else:
                        cursor.execute('SELECT approve FROM tb_tutor WHERE login_id = %s', (results[0],))
                        approve = cursor.fetchone()
                        value = approve[0]
                        if value == 0:
                            return jsonify({'message': 'Wait for approval'})
                        else:
                            return jsonify({'message': f'{user_type} login successfully'})
                else:
                    return jsonify({'message': 'Login failed'})
            else:
                return jsonify({'message': 'Username not found'})
    except Exception as e:
        return jsonify({'Error':str(e)})
    
def viewTutor():
     try:
        cursor.execute('SELECT * FROM tb_tutor')
        tutor = cursor.fetchall()
        return jsonify({'tb_tutor': tutor})
     except Exception as e:
        return jsonify({'Error':str(e)})
def deleteTutor(tutor_id):
    try:
        cursor.execute('SELECT * FROM tb_tutor WHERE tutor_id = %s', (tutor_id,))
        
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'tutor not found with the given ID'}), 404
        cursor.execute('DELETE FROM tb_tutor WHERE tutor_id = %s', (tutor_id,))
        cursor.execute('delete FROM tb_login WHERE login_id = %s', (result[5],))
        db.commit()
        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'Error':str(e)})

def approve(tutor_id):
    try:
        cursor.execute('SELECT * FROM tb_tutor WHERE tutor_id = %s', (tutor_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'tutor not found with the given ID'}), 404
        cursor.execute('UPDATE tb_tutor SET approve = 1 WHERE tutor_id = %s', (tutor_id,))
        db.commit()
        return jsonify({'message': 'Item updated successfully'})
    except Exception as e:
        return jsonify({'Error':str(e)})

def getRewards():
    try:
        cursor.execute('SELECT * FROM tb_rewards')
        rewards = cursor.fetchall()
        return jsonify({'tb_rewards': rewards})
    except Exception as e:
        return jsonify({'Error':str(e)})
def addReward(data):
    try:
        reward_name=data['reward_name']
        is_valid, error_message = check_rewardname(data)
        if not is_valid:
            return jsonify({'error': error_message})
        else:
            cursor.execute('INSERT INTO tb_rewards(reward_name) VALUES (%s)',(reward_name,))
            db.commit()
            return jsonify({'message': 'insert successful'})
    except Exception as e:
        return jsonify({'Error':str(e)})

def deleteReward(reward_id):
    try:
        cursor.execute('SELECT * FROM tb_rewards WHERE reward_id = %s', (reward_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'reward not found with the given ID'}), 404
        cursor.execute('DELETE FROM tb_rewards WHERE reward_id = %s', (reward_id,))
        db.commit()
        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'Error':str(e)})

def getRedeemableitem():
    try:
        cursor.execute('SELECT * FROM tb_item')
        redeemableitem = cursor.fetchall()
        return jsonify({'tb_item': redeemableitem})
    except Exception as e:
        return jsonify({'Error':str(e)})

def addRedeemitem(data):
    try:
        item_name=data['item_name']
        cost=data['cost']
        quantity=data['stock']
        cursor.execute('INSERT INTO tb_item(item_name,cost,stock) VALUES (%s,%s,%s)',(item_name,cost,quantity))
        db.commit()
        return jsonify({'message': 'insert successful'})
    except Exception as e:
        return jsonify({'Error':str(e)})

def deleteRedeemableitem(item_id):
    try:
        cursor.execute('SELECT * FROM tb_item WHERE item_id = %s', (item_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'Id not found'}), 404
        cursor.execute('DELETE FROM tb_item WHERE item_id = %s', (item_id,))
        db.commit()
        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'Error':str(e)})
    
def get_student_badges(student_id):
        # Query to fetch badge details for a student by joining two tables
    try:
        query = """
            SELECT a.attendance_score, b.as_name, b.total_score
            FROM tb_attendance a
            JOIN tb_assessment b ON b.as_id = a.assessment_id
            WHERE a.student_id = %s and a.badge=1;
        """

        cursor.execute(query, (student_id,))
        badges = cursor.fetchall()
        if not badges:
            return jsonify({'error': 'No badge'})
        return badges
    except Exception as e:
        return jsonify({'Error': str(e)})

def get_student_certificates(student_id):
    try:
        # Query to fetch certificate details for a student by joining two tables
        query = """
            SELECT c.c_name, e.e_date AS enrollment_date, e.score AS enrollment_score
            FROM tb_enrollment e
            JOIN tb_course c ON e.course_id = c.course_id
            WHERE e.student_id = %s and certificate=1;
        """

        cursor.execute(query, (student_id,))
        certificates = cursor.fetchall()
        if not certificates:
            return jsonify({'error': 'ID not found'})
        return certificates
    except Exception as e:
        return jsonify({'Error': str(e)})


def search_items_by_name(item_name):
    try:
        # Query to search for items by name
        #query = "SELECT * FROM tb_item WHERE item_name LIKE %s"
        cursor.execute("SELECT * FROM tb_item WHERE item_name LIKE %s",('%' + item_name + '%',),)
        items = cursor.fetchall()
        if not items:
            return jsonify({'error': 'item_name not found'})
        return items
    except Exception as e:
        return jsonify({'Error': str(e)})

def get_student_courses(student_id):
    try:
        # Query to fetch all courses of a student based on enrollment
        query = """
            SELECT c.course_id, c.c_name AS course_name, e.e_date AS enrollment_date, e.score AS enrollment_score, e.status
            FROM tb_enrollment e
            JOIN tb_course c ON e.course_id = c.course_id
            WHERE e.student_id = %s
        """

        cursor.execute(query, (student_id,))
        courses = cursor.fetchall()
        if not courses:
            return jsonify({'error': 'Id not found'})
        return courses
    except Exception as e:
        return jsonify({'Error': str(e)})
         