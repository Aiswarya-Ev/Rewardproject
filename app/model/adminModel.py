# model/program
import bcrypt
from flask import Flask, jsonify, request,session
from flask_bcrypt import check_password_hash
import sys
import os
# Add the parent directory (project_root) to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from configuration.config import db
from validation.validation import *
from utilities.utilities import*
cursor = db.cursor()

def selectAll(tablename):
    try:
        cursor.execute(f'SELECT * FROM {tablename}')
        data = cursor.fetchall()
        if not data:
            return jsonify({'error': 'No data found'})
        
        columns = [col[0] for col in cursor.description]  # Get column names
        data_with_columns = [{columns[i]: row[i] for i in range(len(columns))} for row in data]
        return  generate_response(data_with_columns) # Corrected line
    except Exception as e:
        return jsonify({'Error': str(e)})
def selectById(tablename,fieldname,id):
    try:
        print(tablename,fieldname,id)
        cursor.execute(f"SELECT * FROM {tablename} WHERE {fieldname} = %s",(id,))
        data = cursor.fetchone()
        if not data:
            return jsonify({'error': 'No data found'})
        return data
    except Exception as e:
        return jsonify({'Error': str(e)})
def selectAllStudent():
    try:
        return selectAll("tb_student")
    except Exception as e:
        return jsonify({'Error':str(e)})
def selectAdmin(id):
    try:
        data=selectById("tb_admin","login_id",id)
        structured_items = []
        structured_items.append({
        'id': data[0],
        'username': data[1],
        'phone': data[2]  # Assuming third column is description
        })
        return  generate_response(structured_items)
    except Exception as e:
        return jsonify({'Error':str(e)})           
def registeration(data):
    try:
        name = data.get('name')
        dob = data.get('dob')
        email = data.get('email')
        phone = data.get('phoneNo')
        house = data.get('houseno')
        city = data.get('city')
        state = data.get('state')
        country = data.get('country')  # Corrected variable name
        pin = data.get('pincode')
        username = data.get('username')
        password = data.get('password')
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
            return generate_response()
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
            print(results)
            if results:
                hashed_password = results[2]
                if hashed_password and check_password_hash(hashed_password, user_password):
                    structured_items = []
                    session['id']=results[0]
                    print(session.get('id'))
                    session['type']=results[3]
                    structured_items.append({
                    'id': results[0],
                    'username': results[1],
                    'type': results[3]  # Assuming third column is description
                    })
                    return  generate_response(structured_items)
                else:
                    return generate_response(status_code=401)
            else:
                return generate_response(status_code=401)
    except Exception as e:
        return jsonify({'Error':str(e)})
    
def viewTutor():
     try:
        return selectAll("tb_tutor")
     except Exception as e:
        return jsonify({'Error':str(e)})
def get_tutors_count():
    counts = {}
    # Get tutors count
    query = "SELECT COUNT(*) AS tutor_count FROM tb_tutor"
    cursor.execute(query)
    result = cursor.fetchone()
    counts['tutors'] = result[0] if result else 0
    # Get courses count
    query = "SELECT COUNT(*) AS course_count FROM tb_course"
    cursor.execute(query)
    result = cursor.fetchone()
    counts['courses'] = result[0] if result else 0
    # Get students count
    query = "SELECT COUNT(*) AS student_count FROM tb_student"
    cursor.execute(query)
    result = cursor.fetchone()
    counts['students'] = result[0] if result else 0
    return generate_response(counts)

def deleteTutor(tutor_id):
    try:
        cursor.execute('SELECT * FROM tb_tutor WHERE tutor_id = %s', (tutor_id,))
        
        result = cursor.fetchone()
        if not result:
            return generate_response(status_code=404)
        cursor.execute('DELETE FROM tb_tutor WHERE tutor_id = %s', (tutor_id,))
        cursor.execute('delete FROM tb_login WHERE login_id = %s', (result[5],))
        db.commit()
        return generate_response()
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
        return generate_response()
    except Exception as e:
        return jsonify({'Error':str(e)})

def getRedeemableitem():
    try:
        cursor.execute('SELECT * FROM tb_item')
        redeemableitem = cursor.fetchall()
        structured_items = []
        for item in redeemableitem :
            structured_items.append({
                'id': item[0],
                'name': item[1],
                'cost': item[2], 
                'stock': item[3]})
        return generate_response(structured_items)
    except Exception as e:
        return jsonify({'Error':str(e)})
def getCourse():
    try:
        cursor.execute('SELECT * FROM tb_course')
        redeemableitem = cursor.fetchall()
        structured_items = []
        for item in redeemableitem :
            structured_items.append({
                'id': item[0],
                'name': item[1],
                'date': item[2], 
                'coin': item[3],
                'assessment_no': item[5]})
        return generate_response(structured_items)
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
            return generate_response(status_code=404) 
        cursor.execute('DELETE FROM tb_item WHERE item_id = %s', (item_id,))
        db.commit()
        return generate_response()
    except Exception as e:
        return generate_response(status_code=405)
    
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
        structured_items = []
        for item in certificates :
            structured_items.append({
                'name': item[0],
                'date': item[1], 
                'score': item[2]})
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
         