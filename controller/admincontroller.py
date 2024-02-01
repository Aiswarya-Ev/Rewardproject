# controller/app.py
import sys
import os


# Add the parent directory (project_root) to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from model.adminModel import *
#from validation.datavalidation import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex2023' 
app.config['WTF_CSRF_ENABLED'] = False

@app.route('/api/student', methods=['GET'])
def get_student():
    return selectAllStudent()

@app.route('/api/register', methods=['POST'])
def student_reg():
    data = request.get_json()
    return registeration(data)
    
# Login
@app.route('/api/login', methods=['POST'])
def login():
    data=request.get_json()
    return userlogin(data)

@app.route('/api/tutor', methods=['GET'])
def get_tutor():
    return viewTutor()

@app.route('/api/tutor/<int:tutor_id>', methods=['DELETE'])
def delete_tutor(tutor_id):
    return deleteTutor(tutor_id)

@app.route('/api/tutor/<int:tutor_id>', methods=['PUT'])
def update_item(tutor_id):
    return approve(tutor_id)

@app.route('/api/rewards',methods=['GET'])
def get_rewards():
    return getRewards()

@app.route('/api/rewards',methods=['POST'])
def add_reward():
    data = request.get_json()
    return addReward(data)

@app.route('/api/reward/<int:reward_id>', methods=['DELETE'])
def delete_reward(reward_id):
    cursor.execute('DELETE FROM tb_rewards WHERE reward_id = %s', (reward_id,))
    db.commit()
    return deleteReward(reward_id)

@app.route('/api/redeemitem',methods=['GET'])
def get_redeemableitem():
    return getRedeemableitem()

@app.route('/api/redeemitem',methods=['POST'])
def add_redeemitem():
    data = request.get_json()
    return addRedeemitem(data)

@app.route('/api/redeem/<int:redeemitem_id>', methods=['DELETE'])
def delete_redeemableitem(redeemitem_id):
    return deleteRedeemableitem(redeemitem_id)

# ... (other API routes)

if __name__ == '__main__':
    app.run(debug=True)
