# model/program
import mysql.connector
import bcrypt
from config import mysql_config
from flask import Flask, jsonify, request
from flask_bcrypt import check_password_hash
db = mysql.connector.connect(**mysql_config)
cursor = db.cursor()


def selectAllStudent():
    cursor.execute('SELECT * FROM tb_student')
    student =cursor.fetchall()
    return jsonify({'tb_student': student})

def registeration(data):
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

def userlogin(data):
    username = data.get('username')
    user_password = data.get('userpassword')  # Corrected variable name

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
    
def viewTutor():
     cursor.execute('SELECT * FROM tb_tutor')
     tutor = cursor.fetchall()
     return jsonify({'tb_tutor': tutor})
def deleteTutor(tutor_id):
    cursor.execute('DELETE FROM tb_tutor WHERE tutor_id = %s', (tutor_id,))
    db.commit()
    return jsonify({'message': 'Item deleted successfully'})

def approve(tutor_id):
    cursor.execute('UPDATE tb_tutor SET approve = 1 WHERE tutor_id = %s', (tutor_id,))
    db.commit()
    return jsonify({'message': 'Item updated successfully'})

def getRewards():
    cursor.execute('SELECT * FROM tb_rewards')
    rewards = cursor.fetchall()
    return jsonify({'tb_rewards': rewards})

def addReward(data):
    reward_name=data['reward_name']
    cursor.execute('INSERT INTO tb_rewards(reward_name) VALUES (%s)',(reward_name,))
    db.commit()
    return jsonify({'message': 'insert successful'})

def deleteReward(reward_id):
    cursor.execute('DELETE FROM tb_rewards WHERE reward_id = %s', (reward_id,))
    db.commit()
    return jsonify({'message': 'Item deleted successfully'})

def getRedeemableitem():
    cursor.execute('SELECT * FROM tb_redeemableitem')
    redeemableitem = cursor.fetchall()
    return jsonify({'tb_redeemableitem': redeemableitem})

def addRedeemitem(data):
    item_name=data['item_name']
    cost=data['cost']
    quantity=data['quantity']
    cursor.execute('INSERT INTO tb_redeemableitem(item_name,cost,quantity) VALUES (%s,%s,%s)',(item_name,cost,quantity))
    db.commit()
    return jsonify({'message': 'insert successful'})

def deleteRedeemableitem(redeemitem_id):
    cursor.execute('DELETE FROM tb_redeemableitem WHERE redeemitem_id = %s', (redeemitem_id,))
    db.commit()
    return jsonify({'message': 'Item deleted successfully'})