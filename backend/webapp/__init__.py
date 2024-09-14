# Import relevant modules
from flask import Flask  
from flask_cors import CORS  

from .extns import db  
from .api import api  

# function to create and configure my app
def create_app():  
    # Initialize my flask app
    app = Flask(__name__)  

    # Set up configuration variables
    app.config['SECRET_KEY'] = "secret_key"  
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"  

    # enable Cross-oigin resource sharing 
    CORS(app) 

    # Bind SQLAlchemy to my flask app  
    db.init_app(app)  

    with app.app_context():  
        import webapp.models 
        # Create all  database tables
        db.create_all()  

    # register the API routes using the blueprint
    app.register_blueprint(api)  

    return app  


