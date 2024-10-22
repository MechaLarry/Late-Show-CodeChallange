from flask import Flask
from flask_migrate import Migrate
from config import Config
from routes import api
from extensions import db  # Import db from the new extensions.py

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable debug mode in the app configuration
    app.config['DEBUG'] = True

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(api)

    return app

app = create_app()

# Import models after db is initialized to avoid circular import
from models import Episode, Guest, Appearance

if __name__ == '__main__':
    # Run the app with debug enabled explicitly
    app.run(port=5555, debug=True)
