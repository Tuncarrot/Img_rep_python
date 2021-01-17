## Image Repository

This application is an image repository where users can upload and manage images.

# How do I work?

I run using Python, Flask and SQLAlchemy. You can see me (mostly) working at http://192.53.122.149/ where I'm hosted with a Linux server using Nginx and Gunicorn. If you decide to run me locally, I should be bug-free.

# What do I use?

You will need at least...
-Python 3.5
-Create/use an email with an email application password (https://support.google.com/mail/answer/185833?hl=en).
-Access to a Database with a secret key and database URI

# How can you run me in a Windows Environment?

I'm easy to set up in Windows, just follow along!

Get the repository first
```
git clone https://github.com/Tuncarrot/Img_rep_python.git
```

Install Pip on Windows
https://stackoverflow.com/questions/4750806/how-can-i-install-pip-on-windows provides a good example

Next you will need to set some environment variables to make your code safe to look at. If you dont know how, the following provides a good example. 
https://www.computerhope.com/issues/ch000549.htm

You will need to set the following environment variables and their related values (that you provide)
```
SECRET_KEY
SQLALCHEMY_DATABASE_URI
MAIL_PASS
MAIL_USER
```
Be sure to set the values with your information. If done correctly, the application can pull these values to work properly.

Almost done, create the database next. (you may have to use 'py' instead of 'python' because windows might open the store instead)
```
python
from imgRepFlask import db
db.create_all()
```
You should see a db.site file appear in your project directory

Lastly, we just have to run the application, be sure to be in the project directory for this (Setting debug=1 means the server restarts itself when you make changes to the code)
```
SET FLASK_APP=imgRepFlask
SET FLASK_DEBUG=1
flask run
```

You should have the project running at localhost now!

# How can you run me in a Linux Environment?

Lets start with setting me up from scratch. Assuming you have at least python 3.5 installed. Since the project was intially created on a Windows Environment, there are some extra steps you need, so follow along carefully.

Get the repository first
```
git clone https://github.com/Tuncarrot/Img_rep_python.git
```

Pip for python3
```
sudo apt install python3-pip
```

Virtual Environment (not required but if you want to be proper)
```
sudo apt install python3-venv
```

if you installed the virtual environment, create one with
```
python3 -m venv imgRepPython/venv
```

and activate it with
```
source venv/bin/activate
```

If the viritual environment is active, you should see (venv) infront of your username on your console.

Now install all the prerequisites from the requirements.txt file (be in the project directory)
```
pip install -r requirements.txt
```

Next we will need to set the configuration file to allow the local copy to function properly
```
sudo touch /etc/config.json
sudo nano /etc/config.json
```

Here we will store all the configurable data, copy as needed
```
{
    "SECRET_KEY":"TOP-SECRET-KEY"
    "SQLALCHEMY_DATABASE_URI":"TOP-SECRET-DATABASE-URI"
    "EMAIL_USER": "YOUR-EMAIL"
    "EMAIL_PASS": "YOUR-PASSWORD"
}
```

*NOTE - When entering your password you may have to create and enable an application key within your email settings, and use this key instead of your actual password

Next we will configure our configuration file to read from the one we just created, modify the file as needed (this file needs to be changed due to the original being developed in a Windows environment)
```
sudo nano /imgRepFlask/config.py
```
Inside the file, make sure the following matches
```
import os
import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)

class Config:
    SECRET_KEY = config.get('SECRET_KEY') 
    SQLALCHEMY_DATABASE_URI =config.get('SQLALCHEMY_DATABASE_URI')  
    CORS_HEADERS = 'Content-Type'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('MAIL_USER')
    MAIL_PASSWORD = config.get('MAIL_PASS')
```
*Note how for this example, os.environ.get was replaced with config.get

Next we will need to create the database in order to see the application functioning properly, and we can do this in the python interpreter
```
python
from imgRepFlask import db, create_app
app = create_app()
app.app_context().push()
db.create_all()
```
You should see a site.db file created in the project directory.
Nice! We are ready to run this program in a development environment! Be sure to be in the project directory for the next part.
```
export FLASK_APP=run.py
flask run -host=0.0.0.0
```

You should be able to see the application in your browser at your IP address with port 5000!


## Useful commands during development (for windows command line)

(be in project directory)

SET FLASK_APP=fitnessAppFlask.py

SET FLASK_DEBUG=1

flask run

# Create Database

(be in project directory)

from imgRepFlask import db
db.create_all()

- this will create the database

