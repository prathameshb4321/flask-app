# ---------- Flask App Factory ----------
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'replace-me-in-prod'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    # Create tables
    with app.app_context():
        db.create_all()

    return app
