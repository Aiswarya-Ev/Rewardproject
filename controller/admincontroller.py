# controller/app.py
import sys
import os

# Add the parent directory (project_root) to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from model.adminModel import *
app = Flask(__name__)

@app.route('/api/student', methods=['GET'])
def get_student():
    return selectAllStudent()

# ... (other API routes)

if __name__ == '__main__':
    app.run(debug=True)
