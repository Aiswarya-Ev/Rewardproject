import mysql.connector
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from validation.studentValidation import *
from configuration.config import mysql_config
from utilities.utilities import*
from flask import Flask, jsonify, request

def student(student_id):
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tb_student WHERE student_id = %s', (student_id,))
        student = cursor.fetchone()
 
        if student is None:
            return jsonify({'message': 'student not found'}), 404
 
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided in the request'}), 400
        
        
        # Update only the fields provided in the JSON payload
        updated_fields = []
        for key, value in data.items():
            cursor.execute(f'UPDATE tb_student SET {key} = %s WHERE student_id = %s', (value, student_id))
            updated_fields.append(key)
            db.commit()
        is_valid, validation_errors = validate_update_student(data)
        if not is_valid:
            return jsonify({'message': 'Validation failed', 'errors': validation_errors}), 400
        db.commit()

        return jsonify({'message': 'student data updated successfully', 'updated_fields': updated_fields})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()
def get_details(student_id):
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
        badges = get_student_badges_count(student_id)
        certificates = get_student_certificates_count(student_id)
        coins = get_student_coins(student_id)
        #details = select_student_details(student_id)
        
        # Combine all details into a dictionary
        student_details = {
            'badges': badges,
            'certificates': certificates,
            'coins': coins
        }
        print(student_details)
        return generate_response(student_details)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()
def getCourse(student_id):
    db = mysql.connector.connect(**mysql_config)
    cursor = db.cursor()
    cursor.execute('''
        SELECT 
            c.course_id,
            c.c_name,
            e.e_date,
            c.coins,
            c.tutor_id,
            c.assessment_no
        FROM 
            tb_course c
        INNER JOIN 
            tb_enrollment e ON c.course_id = e.course_id 
        WHERE 
            e.student_id = %s
            AND e.status = 'Booked'
    ''', (student_id,))
    
    info = cursor.fetchall()
    structured_items = []
    for data in info:
        structured_items.append({
            'course_id': data[0],
            'c_name': data[1],
            'start_date': data[2],
            'coins': data[3],
            'tutor_id': data[4],
            'assessment_no': data[5]
        })

    return generate_response(structured_items)
def get_unenrolled_courses(student_id):
    db = mysql.connector.connect(**mysql_config)
    cursor = db.cursor()
    cursor.execute('''
        SELECT 
            c.course_id,
            c.c_name,
            c.start_date,
            c.coins,
            c.tutor_id,
            c.assessment_no
        FROM 
            tb_course c
        LEFT JOIN 
            tb_enrollment e ON c.course_id = e.course_id AND e.student_id = %s
        WHERE 
            e.student_id IS NULL
    ''', (student_id,))
    
    info = cursor.fetchall()
    structured_items = []
    for data in info:
        structured_items.append({
            'course_id': data[0],
            'c_name': data[1],
            'start_date': data[2],
            'coins': data[3],
            'tutor_id': data[4],
            'assessment_no': data[5]
        })

    return generate_response(structured_items)
def showItem():
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
        cursor.execute('SELECT * from tb_item')
        showritem = cursor.fetchall()
        if not showritem:
            return jsonify({'error': 'Id not found'}), 404
        return jsonify({'showritem': showritem})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()
    

def purchase(item_id, student_id):
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
        # Check if the item is in stock
        cursor.execute('SELECT cost, stock FROM tb_item WHERE item_id = %s', (item_id,))
        item_data = cursor.fetchone()
        if not item_data:
            return jsonify({'message': 'Item not found'})
        
        if item_data and item_data[1] > 0:
            cost, stock = item_data
            
            # Check if the student has enough Supercoins
            cursor.execute('SELECT coins FROM tb_supercoin WHERE student_id = %s', (student_id,))
            student_coins = cursor.fetchone()
            if not student_coins:
                return jsonify({'message': 'student_id not found'})
            if student_coins and student_coins[0] >= cost:
                
                # Decrement the stock of the selected item
                cursor.execute('UPDATE tb_item SET stock = stock - 1  WHERE item_id = %s', (item_id,))
                db.commit()
                # Deduct the cost from the student's Supercoins
                cursor.execute('UPDATE tb_supercoin SET coins = coins - %s WHERE student_id = %s', (cost, student_id))
                db.commit()
                # Update the Redeem table
                cursor.execute('INSERT INTO tb_transaction (student_id, item_id, transaction_date) VALUES (%s, %s, CURDATE())', (student_id, item_id))
                db.commit()
                return jsonify({'message': 'Item selected successfully'})
            else:
                return jsonify({'message': 'Not enough Supercoins to purchase this item'})
        else:
            return jsonify({'message': 'Item is out of stock'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()

def enrollmentPost(course_id,student_id):
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
        status = 'Booked'
        cursor.execute("select * from tb_enrollment where student_id=%s and course_id=%s",(student_id,course_id))
        check=cursor.fetchone()
        if check:
            return jsonify({'message': 'Already entrolled'})
        cursor.execute('INSERT INTO tb_enrollment (e_date, status, course_id, student_id) VALUES (CURDATE(), %s, %s, %s)',(status, course_id, student_id))
        db.commit()
        return generate_response()
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()
    
def get_student_badges(student_id):
        # Query to fetch badge details for a student by joining two tables
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
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
        print(badges)
        return badges
    except Exception as e:
        return jsonify({'Error': str(e)})
def get_student_badges_count(student_id):
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
        # Query to count the number of badges for a student
        query = """
            SELECT COUNT(*) AS badge_count
            FROM tb_attendance
            WHERE student_id = %s and badge = 1;
        """

        cursor.execute(query, (student_id,))
        badge_count = cursor.fetchone()[0]
        return badge_count
    except Exception as e:
        return jsonify({'Error': str(e)})
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()

def get_student_certificates(student_id):
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
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
        print(certificates)
        return certificates
    except Exception as e:
        return jsonify({'Error': str(e)})
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()
def get_student_certificates_count(student_id):
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
        # Query to count the number of certificates for a student
        query = """
            SELECT COUNT(*) AS certificate_count
            FROM tb_enrollment
            WHERE student_id = %s and certificate = 1;
        """

        cursor.execute(query, (student_id,))
        certificate_count = cursor.fetchone()[0]
        return certificate_count
    except Exception as e:
        return jsonify({'Error': str(e)})
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()
def get_student_coins(student_id):
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
        cursor.execute('SELECT  coins FROM tb_supercoin  WHERE student_id = %s', (student_id,))
        student_coin = cursor.fetchone()
        if not student_coin:
            return jsonify({'error': 'Id not found'}), 404
        print(student_coin)
        return student_coin[0]
    except Exception as e:
        return jsonify({'error': str(e)}), 500  
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()
def select_student_details(tablename,fieldname,student_id):
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
        'house_no': data[0][5],
          'city': data[0][6],
        'state': data[0][7],
        'country': data[0][8],
          'pin': data[0][9],
        'login': data[0][10]   # Assuming third column is description
        })
        return generate_response(structured_items)
    except Exception as e:
        return jsonify({'Error':str(e)}) 
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()

def get_student_certificates(student_id):
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
        # Query to fetch certificate details for a student by joining two tables
        query = """
            SELECT c.c_name, e.e_date AS enrollment_date, e.score AS enrollment_score
            FROM tb_enrollment e
            JOIN tb_course c ON e.course_id = c.course_id
            WHERE e.student_id = %s and certificate!=-1;
        """

        cursor.execute(query, (student_id,))
        certificates = cursor.fetchall()
        if not certificates:
            return generate_response(status_code=404)
        structured_items = []
        for item in certificates :
            structured_items.append({
                'name': item[0],
                'date': item[1], 
                'score': item[2]})
        return generate_response(structured_items)
    except Exception as e:
        return jsonify({'Error': str(e)}) 
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()    
def getAssessment(course_id,student_id):
    db = mysql.connector.connect(**mysql_config)
    cursor = db.cursor()
    query = """
    SELECT 
    a.as_id,a.coins,a.total_score,
    a.as_name,
    CASE 
        WHEN at.student_id IS NOT NULL THEN 1
        ELSE 0
    END AS status
FROM 
    tb_assessment a
LEFT JOIN 
    tb_attendance at ON a.as_id = at.assessment_id AND at.student_id = %s
WHERE 
    a.course_id = %s

    """
    cursor.execute(query,(student_id, course_id))
    assessment_list = cursor.fetchall()
    structured_items = []
    for item in assessment_list:
        structured_items.append({
            'assessment_no': item[0],
            'coins': item[1], 
            'total_score': item[2],
            'as_name':item[3],
            'status':item[4]})  # Call the fetchall method to retrieve the data
    # Convert the fetched data into a list of dictionaries
    #print(assessment_list)
    return generate_response(structured_items)
    
def get_items_by_student_id(student_id):
    db = mysql.connector.connect(**mysql_config)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tb_item JOIN tb_transaction ON tb_item.item_id = tb_transaction.item_id WHERE tb_transaction.student_id = %s", (student_id,))
    items = cursor.fetchall()
    structured_items = []
    for item in items:
        structured_items.append({
            'item_id': item[0],
            'item_name': item[1], 
            'cost': item[2],
            'stock':item[3],
            'transation_id':item[4],
            'transation_date': item[5],
            'student_id': item[6], 
            'item_id': item[7]
            })
    return generate_response(structured_items)
def getPurchaseitem():
    try:
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tb_item WHERE stock > 0')
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
    finally:
        # Close database connection
        if db.is_connected():
            cursor.close()
            db.close()

