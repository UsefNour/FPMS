from flask import Flask
from models import db, User
from extensions import login_manager, socketio
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fpms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.jinja_env.filters['load_json'] = json.loads
app.jinja_env.filters['strftime'] = lambda d, fmt: d.strftime(fmt) if d else ''
app.jinja_env.globals['now'] = datetime.utcnow

@app.template_filter('nl2br')
def nl2br_filter(s):
    if not s:
        return s
    return s.replace('\n', '<br>')

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
socketio.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Register blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.training import training_bp
from routes.social import social_bp
from routes.fighters import fighters_bp
from routes.sparring import sparring_bp
from routes.events import events_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(training_bp)
app.register_blueprint(social_bp)
app.register_blueprint(fighters_bp)
app.register_blueprint(sparring_bp)
app.register_blueprint(events_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
