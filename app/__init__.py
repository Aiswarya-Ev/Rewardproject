from flask import Flask
from controller.admincontroller import admin_blueprint
from controller.studentController import student_blueprint
from controller.tutorController import tutor_blueprint
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thecodex2023' 
    app.config['WTF_CSRF_ENABLED'] = False
    app.config.from_pyfile('configuration/config.py')

    # Register blueprints
    app.register_blueprint(admin_blueprint, url_prefix='/api/admin')
    app.register_blueprint(tutor_blueprint, url_prefix='/api/tutor')
    app.register_blueprint(student_blueprint, url_prefix='/api/student')

    return app
