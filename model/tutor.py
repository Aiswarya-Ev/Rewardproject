import mysql.connector #connect sql
from flask import Flask, jsonify, request #convert Python dictionaries to JSON format 
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from config import mysql_config
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
    


