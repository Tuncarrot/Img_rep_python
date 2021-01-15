import os, binascii
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from imgRepFlask import mail, constants
#import secrets


def save_picture(form_picture): #Move this into seperate file, along with db query/submit/connection stuff
    random_hex = binascii.b2a_hex(os.urandom(4)).decode("utf-8")
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    i = Image.open(form_picture)
    i=i.resize((constants.IMG_PIXEL_HEIGHT, constants.IMG_PIXEL_WIDTH), Image.ANTIALIAS)
    i.save(picture_path)
    return picture_fn

def send_email_reset(user, accountInfo):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='focalpointimagerep@gmail.com', recipients=[accountInfo.email])
    email_msg = "Visit the following link to reset your password\n{URL_LINK}\nIf you did not send this request, please ignore."
    msg.body = email_msg.format(URL_LINK = {url_for('users.reset_token', token=token, _external=True)})
    mail.send(msg)

def save_image(form_picture): #Move this into seperate file, along with db query/submit/connection stuff
    filename = form_picture.filename
    random_hex = binascii.b2a_hex(os.urandom(4)).decode("utf-8")
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/uploaded_pics', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn
