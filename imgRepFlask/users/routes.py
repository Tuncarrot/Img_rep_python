from __future__ import print_function
import os, binascii, sys
from flask import render_template, url_for, flash, redirect, request, Blueprint # import render_template function for rendering HTML pages individually, url 4 for finding files in the background
from imgRepFlask import db, bcrypt, constants
from imgRepFlask.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, PasswordResetForm
from imgRepFlask.models import User, Account, ContactInfo                      # Using models in views, DB needs to exist first
from flask_login import login_user, current_user, logout_user, login_required
from imgRepFlask.users.utils import save_picture, send_email_reset

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])       
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
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
        return redirect(url_for('users.login')) #redirect to function name of route
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])         
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(email = form.email.data).first()                    # Check if email exists, grab user
        if user and bcrypt.check_password_hash(user.password, form.password.data):      # Compare User saved password with entered password
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')                                        # Grab url parameter
            return redirect(next_page) if next_page else redirect(url_for('main.home_page')) # Redirect to original page the user was trying to access
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')      
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')         
def logout():
    logout_user()            
    return redirect(url_for('main.home_page'))

@users.route('/account/updateInfo', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account_home'))
    elif request.method == 'GET':
        account_data = Account.query.filter_by(id=current_user.id).first()
        contactInfo_data = ContactInfo.query.filter_by(id=current_user.id).first()
        form.name.data = contactInfo_data.name
        form.email.data = account_data.email
    image_file= url_for('static', filename='profile_pics/' + account_data.image_file)          
    return render_template('/account/updateInfo.html', title='Account', image_file=image_file, form=form)

@users.route('/account/home', methods=['GET', 'POST'])
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

@users.route('/account/reset_password', methods=['GET', 'POST'])      
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = RequestResetForm()
    if form.validate_on_submit():
        userAccount = Account.query.filter_by(email=form.email.data).first()
        user = User.query.filter_by(id=userAccount.user_id).first()
        print(user, sep='\n', file=sys.stderr)
        send_email_reset(user, userAccount)
        flash('Password reset email sent!', 'info')
        return redirect(url_for('users.login'))
    return render_template('/account/reset_request.html', title="Reset Password", form=form)

@users.route('/account/reset_password/<token>', methods=['GET', 'POST'])      
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Token is invalid or expired!', 'danger')
        return redirect(url_for('users.reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        account = Account.query.filter_by(user_id=user.id).first()
        account.password = hashed_password
        db.session.commit()
        flash('Your password has been reset', 'success')
        return redirect(url_for('users.login')) #redirect to function name of route
    return render_template('/account/reset_token.html', title="Reset Password", form=form)
