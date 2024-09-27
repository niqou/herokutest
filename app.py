import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Initialize Flask-Mail
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

app.secret_key = 'testsecretkkey'  # define this in somethinng safer

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    msg = Message('New Contact Form Submission',
                  sender=os.getenv('MAIL_USERNAME'),   #define somewhere safe
                  recipients=[os.getenv('RECIPENT_EMAIL')])  #define somewhere safe
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    mail.send(msg)

    flash('Your message has been sent successfully!')
    return redirect(url_for('home'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Debug prints
        print(f"Attempting login with username: {username}")
        print(f"Password provided: {password}")

        user = User.query.filter_by(username=username).first()

        if user:
            print(f"User found: {user.username}")
            print(f"Stored password hash: {user.password}")
            if check_password_hash(user.password, password):
                print("Password is correct")
                login_user(user)
                return redirect(url_for('admin_dashboard'))
            else:
                print("Password is incorrect")
                flash('Invalid username or password')
        else:
            print("User not found")
            flash('Invalid username or password')

    return render_template('admin.html')

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
   with app.app_context():
    db.create_all()
app.run()
