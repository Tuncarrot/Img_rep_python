
from __future__ import print_function
import os, binascii, sys
from PIL import Image
from flask import render_template, url_for, flash, redirect, request # import render_template function for rendering HTML pages individually, url 4 for finding files in the background
from imgRepFlask import app, db, bcrypt, constants
from imgRepFlask.forms import RegistrationForm, LoginForm, UpdateAccountForm, UploadPhotoForm
from imgRepFlask.models import User, Account, ContactInfo, Album, Picture                          # Using models in views, DB needs to exist first
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')             # routes
@app.route('/home')            
def home_page():
    return render_template('home.html', title='Welcome')

@app.route('/about')         
def about_page():
    return render_template('about.html', title='About')

@app.route('/browse')
@login_required
def browse_page():
    images = list()
    albums = Album.query.filter_by(user_id=current_user.id).all()
    print(albums, sep='\n', file=sys.stderr)
    if not albums:
        flash('There are currently no albums to view, add an album first!', 'danger')
        return redirect(url_for('home_page'))
    else:
        for album in albums:
            photos = Picture.query.filter_by(album_id=album.id).first()
            images.append(photos)
            print(images, sep='\n', file=sys.stderr)
        return render_template('browse.html', title='Browse Photos', photos = images)



@app.route('/register', methods=['GET', 'POST'])       
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User() #album is not required to make user
        #user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        contactInfo = ContactInfo(name=form.name.data, creator=user)
        account = Account(email=form.email.data, password=hashed_password, creator=user)
        db.session.add(contactInfo)
        db.session.add(account)
        db.session.commit()
        flash('Welcome {0}, your account has been created!'.format(form.name.data), 'success')
        return redirect(url_for('login')) #redirect to function name of route
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])         
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(email = form.email.data).first()                    # Check if email exists, grab user
        if user and bcrypt.check_password_hash(user.password, form.password.data):      # Compare User saved password with entered password
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')                                        # Grab url parameter
            return redirect(next_page) if next_page else redirect(url_for('home_page')) # Redirect to original page the user was trying to access
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')      
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')         
def logout():
    logout_user()            
    return redirect(url_for('home_page'))

def save_picture(form_picture): #Move this into seperate file, along with db query/submit/connection stuff
    random_hex = binascii.b2a_hex(os.urandom(4)).decode("utf-8")
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    i = Image.open(form_picture)
    i=i.resize((constants.IMG_PIXEL_HEIGHT, constants.IMG_PIXEL_WIDTH), Image.ANTIALIAS)
    i.save(picture_path)
    return picture_fn

@app.route('/account/updateInfo', methods=['GET', 'POST'])
@login_required
def account_updateInfo():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        user_account = Account.query.filter_by(id=current_user.id).first()
        user_contact = ContactInfo.query.filter_by(id=current_user.id).first()
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user_account.image_file = picture_file
            #current_user.image_file = picture_file
        user_contact.name = form.name.data
        user_account.email = form.email.data
        db.session.commit()
        flash('Account Details Updated', 'success')
        return redirect(url_for('account_home'))
    elif request.method == 'GET':
        account_data = Account.query.filter_by(id=current_user.id).first()
        contactInfo_data = ContactInfo.query.filter_by(id=current_user.id).first()
        form.name.data = contactInfo_data.name
        form.email.data = account_data.email
    image_file= url_for('static', filename='profile_pics/' + account_data.image_file)          
    return render_template('/account/updateInfo.html', title='Account', image_file=image_file, form=form)

@app.route('/account/home', methods=['GET', 'POST'])
@login_required         
def account_home():
    form = UpdateAccountForm()
    user_account = Account.query.filter_by(id=current_user.id).first()
    user_contact = ContactInfo.query.filter_by(id=current_user.id).first()
    if request.method == 'GET':
        form.name.data = user_contact.name
        form.email.data = user_account.email
    image_file= url_for('static', filename='profile_pics/' + user_account.image_file)          
    return render_template('/account/home.html', title='Account', image_file=image_file, form=form)


@app.route('/upload', methods=['GET', 'POST'])
@login_required         
def upload_image():
    form = UploadPhotoForm()
    if form.validate_on_submit():
        album = Album(name = form.name.data, date = form.date.data, user_id=current_user.id)
        db.session.add(album)
        for file in form.image_file.data:
            image = Picture(name = form.name.data, image_file = save_image(file), poster=album)
            db.session.add(image)
        db.session.commit()
        flash('Photos have been uploaded!', 'success')
        return redirect(url_for('upload_image'))
    return render_template('upload.html', title='Upload Photos', form=form)

def save_image(form_picture): #Move this into seperate file, along with db query/submit/connection stuff
    filename = form_picture.filename
    random_hex = binascii.b2a_hex(os.urandom(4)).decode("utf-8")
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploaded_pics', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    print("Save " + filename + " to " + picture_path, file=sys.stderr)
    return picture_fn

@app.route('/album/<int:album_id>')
@login_required         
def album(album_id):
    photos = Picture.query.filter_by(album_id=album_id).all()
    return render_template('album.html', title="Browse Album", photos = photos)

# Delete all photos first, then album
@app.route("/album/<int:album_id>/delete", methods=['GET'])
@login_required
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        abort(403)
    photos = Picture.query.filter_by(album_id=album_id).all()
    for photo in photos:
        db.session.delete(photo)
    print(album, sep='\n', file=sys.stderr)
    db.session.delete(album)
    db.session.commit()
    flash('Album has been deleted!', 'success')
    return redirect(url_for('home_page'))

# Delete photo, echk if album is empty, if so, delete album/
@app.route("/album/<int:album_id>/<int:picture_id>/delete", methods=['GET'])
@login_required
def delete_picture(album_id, picture_id):
    album = Album.query.get_or_404(album_id)                                # Get album object                            # Grab selected photo                                              # Store album id
    if album.user_id != current_user.id:                                    # Check if user is allowed to access
        abort(403)
    photo = Picture.query.get_or_404(picture_id)
    album_id = photo.album_id 
    db.session.delete(photo)                                                # Delete
    last_photo_check = Picture.query.filter_by(album_id=album_id).all()     # Check if photos exist with album id
    if not last_photo_check:
        db.session.delete(album)                                            # Delete album
    db.session.commit() 
    flash('Photo has been deleted!', 'success')
    return redirect(url_for('browse_page'))