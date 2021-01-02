from datetime import datetime
from imgRepFlask import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# # SQL MODELS
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg') #profile pictures
#     password =  db.Column(db.String(60), nullable = False) # 60 characters due to hash
#     calories = db.relationship('Calorie', backref='user', lazy=True) # Creates a user column in Calorie, to link two tables together. Lazy true means data is loaded in 1 go

#     def __repr__(self): # How our object is printed
#         return 'User("{0}, {1}, {2}")'.format(self.name, self.email, self.image_file)

# class Calorie(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     calorie = db.Column(db.Integer)
#     processed_sugar =  db.Column(db.Integer)
#     protein =  db.Column(db.Integer)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Pass function as the argument, not include () because that would get time now
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self): # How our object is printed
#         return 'Calorie("Calories: {0}, Processed Sugar: {1},Protein: {2}, Date: {3}")'.format(self.calorie, self.processed_sugar, self.protein, self.date)

class User(db.Model, UserMixin): #UserMixin?
    id = db.Column(db.Integer, primary_key=True)
    contactInfo = db.relationship('ContactInfo', backref='user', uselist=False)
    account = db.relationship('Account', backref='user', uselist=False) #uselist=false means 1-1 relationship
    album = db.relationship('Album', backref='user', lazy=True)

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password =  db.Column(db.String(60), nullable = False) # 60 characters due to hash
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') #profile pictures
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pictures = db.relationship('Picture', backref='album', lazy=True)

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    date = db.Column(db.DateTime)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
