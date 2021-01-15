from flask import render_template, request, Blueprint # import render_template function for rendering HTML pages individually, url 4 for finding files in the background

main = Blueprint('main', __name__)

@main.route('/')             # routes
@main.route('/home')            
def home_page():
    return render_template('home.html', title='Welcome')

@main.route('/about')         
def about_page():
    return render_template('about.html', title='About')

