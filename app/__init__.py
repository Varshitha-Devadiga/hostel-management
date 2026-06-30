from flask import Flask
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import DevelopmentConfig
from jinja2 import ChoiceLoader, FileSystemLoader

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    # Extend template search path to include external student registration templates
    app.jinja_loader = ChoiceLoader([
        app.jinja_loader,
        FileSystemLoader(r'E:/bcwd/student_regist')
    ])
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login_student'
    login_manager.login_message_category = 'danger'
    migrate.init_app(app, db)

    # User loader - import inside function to avoid circular import
    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .auth import auth_bp
    from .student import student_bp
    from .admin import admin_bp
    from .staff.routes import bp as staff_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)

    return app
