import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from app.__init__ import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
