from flask import Flask # Import flask as Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from imgRepFlask.config import Config

# Declare here, but intialize in function
CORS()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

# create function to run app to create instances with different
# configurations (development/production), also factory pattern
def create_app(config_class=Config):
    app = Flask(__name__)   # Declare app variable, set instance of flask class (double underscore is a special name for the module)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from imgRepFlask.users.routes import users  
    from imgRepFlask.images.routes import images
    from imgRepFlask.main.routes import main
    from imgRepFlask.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(images)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

# dont move extensions into app creation function due to extension object not getting 
# bound to the application, w/ this design pattern, no app specific state is stored on the
# extension object, so 1 extension object can be used for multiple apps