from flask import Flask # Import flask as Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)                                       # Declare app variable, set instance of flask class (double underscore is a special name for the module)

app.config['SECRET_KEY'] = '4v8r9asfe52987fd5'              # Should be random characters
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # 3 slashes means relative path
 
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from imgRepFlask import routes
