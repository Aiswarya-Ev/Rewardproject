import mysql.connector
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from validation.studentValidation import *
from configuration.config import mysql_config
from flask import Flask, jsonify, request
db = mysql.connector.connect(**mysql_config)
cursor = db.cursor()


def student(student_id):
    try:
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
        is_valid, validation_errors = validate_update_student(data)
        if not is_valid:
            return jsonify({'message': 'Validation failed', 'errors': validation_errors}), 400
        db.commit()

        return jsonify({'message': 'student data updated successfully', 'updated_fields': updated_fields})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
  

# def studentReward(student_id):
#     try:
#         cursor.execute('SELECT tb_rewards.reward_name FROM tb_rewards JOIN tb_studentreward ON tb_rewards.reward_id = tb_studentreward.reward_id WHERE tb_studentreward.student_id = %s', (student_id,))
#         student_rewards = cursor.fetchall()
#         if not student_rewards:
#             return jsonify({'error': 'Student not found with the given ID'}), 404
#         return jsonify({'student_rewards': student_rewards})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500  
    

def showItem():
    try:
        cursor.execute('SELECT * from tb_item')
        showritem = cursor.fetchall()
        if not showritem:
            return jsonify({'error': 'Id not found'}), 404
        return jsonify({'showritem': showritem})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
    

def purchase(item_id, student_id):
    try:
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

                # Deduct the cost from the student's Supercoins
                cursor.execute('UPDATE tb_supercoin SET coins = coins - %s WHERE student_id = %s', (cost, student_id))
                
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
    

def studentCoin(student_id):
    try:
        cursor.execute('SELECT tb_supercoin.coins FROM tb_supercoin  WHERE tb_supercoin.student_id = %s', (student_id,))
        student_coin = cursor.fetchall()
        if not student_coin:
            return jsonify({'error': 'Id not found'}), 404
        return jsonify({'student_coin': student_coin})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  
    

def enrollmentPost():
    try:
        data = request.get_json()
        status = 'Booked'
        course_id = data.get('course_id')
        student_id = data.get('student_id')
        cursor.execute("select * from tb_enrollment where student_id=%s and course_id=%s",(student_id,course_id))
        check=cursor.fetchone()[0]
        if check:
            return jsonify({'message': 'Already entrolled'})
        cursor.execute('INSERT INTO tb_enrollment (e_date, status, course_id, student_id) VALUES (CURDATE(), %s, %s, %s)',( status, course_id, student_id))
        db.commit()
        return jsonify({'message': 'Data added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
     

# def attendanceGet():
#     try:
#         cursor.execute('SELECT * FROM tb_attendance')
#         attendance = cursor.fetchall()
#         return jsonify({'attendance': attendance})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500  
    

# def attendanceAdd():
#     try:
#         data = request.get_json()
#         badge = data.get('badge') 
#         attendance_score = data.get('attendance_score')
#         student_id = data.get('student_id') 
#         assessment_id = data.get('assessment_id') 
#         total_score = data.get('total_score')
#         cursor.execute('INSERT INTO tb_attendance (badge, attendance_score, student_id, assessment_id, total_score) VALUES (%s, %s, %s, %s, %s)', (badge, attendance_score,student_id, assessment_id, total_score))
#         db.commit()
#         return jsonify({'message': 'Data added successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500 
    

# def badge():
#     try:
#         data = request.get_json()
#         attendance_score = data.get('attendance_score')
#         student_id = data.get('student_id') 
#         assessment_id = data.get('assessment_id') 

#         # Check if attendance_score is more than 5
#         badge = 1 if attendance_score > 5 else 0

#         cursor.execute('INSERT INTO tb_attendance (badge,attendance_score, student_id, assessment_id) VALUES (%s, %s, %s, %s)', (badge, attendance_score, student_id, assessment_id))
#         db.commit()

#         return jsonify({'message': 'Data added successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500  