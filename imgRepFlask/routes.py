import os, binascii
from PIL import Image
from flask import render_template, url_for, flash, redirect, request # import render_template function for rendering HTML pages individually, url 4 for finding files in the background
from imgRepFlask import app, db, bcrypt, constants
from imgRepFlask.forms import RegistrationForm, LoginForm, UpdateAccountForm
from imgRepFlask.models import User, Calorie                            # Using models in views, DB needs to exist first
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author':'blah',
        'title':'post 1',
        'content':'first post',
        'date_created':'today'
    },
    {
        'author':'blah2',
        'title':'post 21',
        'content':'second post',
        'date_created':'today'
    }
]

@app.route('/')             # routes
@app.route('/home')            
def home_page():
    return render_template('home.html', title='Welcome', posts = posts)

@app.route('/about')         
def about_page():
    return render_template('about.html', title='About')

@app.route('/browse')            
def browse_page():
    return render_template('browse.html', title='Welcome', posts = posts)

@app.route('/register', methods=['GET', 'POST'])         
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
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
        user = User.query.filter_by(email = form.email.data).first()                    # Check if email exists, grab user
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
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Details Updated', 'success')
        return redirect(url_for('account_home'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)          
    return render_template('/account/updateInfo.html', title='Account', image_file=image_file, form=form)

@app.route('/account/home', methods=['GET', 'POST'])
@login_required         
def account_home():
    form = UpdateAccountForm()
    if request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)          
    return render_template('/account/home.html', title='Account', image_file=image_file, form=form)

    