# Image Repository

This application runs in python, in an attempt to learn python

# What do I do?

Here you can upload images

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

