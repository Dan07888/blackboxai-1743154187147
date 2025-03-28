from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

# Import routes and models after db initialization to avoid circular imports
from routes import *
from models import *

if __name__ == '__main__':
    # Ensure instance directory exists with proper permissions
    os.makedirs('instance', exist_ok=True, mode=0o755)
    
    with app.app_context():
        db.create_all()
        # Create default admin user if none exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
    app.run(host='0.0.0.0', port=8000, debug=True)
