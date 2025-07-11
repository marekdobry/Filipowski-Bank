from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# ----------------------------------
# App and Database Configuration
# ----------------------------------

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 🔒 Change this in production!

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------------------
# Database Models
# ----------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

# ----------------------------------
# Routes
# ----------------------------------


@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# ---------- Register ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# ---------- Login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user'] = user.email
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')

    return render_template('login.html')

# ---------- Dashboard ----------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['user']).first()
    return render_template('dashboard.html', user=user)

# ---------- Balance Update ----------
@app.route('/update_balance', methods=['POST'])
def update_balance():
    if 'user' not in session:
        flash('You must be logged in to update balance.', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['user']).first()
    
    try:
        amount = float(request.form['amount'])
        user.balance += amount
        db.session.commit()
        flash(f'Balance updated by ${amount:.2f}', 'success')
    except ValueError:
        flash('Invalid amount entered.', 'error')

    return redirect(url_for('dashboard'))

# ---------- Logout ----------
@app.route('/logout', methods=['POST'])
def logout():
    flash('You have been logged out.', 'success')
    session.clear()
    return redirect(url_for('login'))

# ---------- Transfer Funds ----------
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'user' not in session:
        flash('You must be logged in to transfer funds.', 'error')
        return redirect(url_for('login'))

    sender = User.query.filter_by(email=session['user']).first()

    if request.method == 'POST':
        recipient_email = request.form['recipient']
        try:
            amount = float(request.form['amount'])
        except ValueError:
            flash('Invalid amount entered.', 'error')
            return redirect(url_for('transfer'))

        if amount <= 0:
            flash('Amount must be greater than zero.', 'error')
            return redirect(url_for('transfer'))

        if amount > sender.balance:
            flash('Insufficient funds.', 'error')
            return redirect(url_for('transfer'))

        recipient = User.query.filter_by(email=recipient_email).first()
        if not recipient:
            flash('Recipient not found.', 'error')
            return redirect(url_for('transfer'))

        # Perform transfer
        sender.balance -= amount
        recipient.balance += amount
        db.session.commit()

        flash(f'Successfully transferred ${amount:.2f} to {recipient.email}', 'success')
        return redirect(url_for('dashboard'))

    return render_template('transfer.html', user=sender)


# ----------------------------------
# App Entry Point
# ----------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
