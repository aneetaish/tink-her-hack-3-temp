# app.py
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///babyconnect.db'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    dob = db.Column(db.Date)
    pregnancy_weeks = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    medications = db.relationship('Medication', backref='user', lazy=True)

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    phone = request.form['phone']
    user = User.query.filter_by(phone=phone).first()
    
    if not user:
        user = User(phone=phone)
        db.session.add(user)
        db.session.commit()
    
    session['user_id'] = user.id
    return redirect('/home')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    user = User.query.get(session['user_id'])
    return render_template('home.html', user=user)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect('/')
    
    user = User.query.get(session['user_id'])
    user.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
    user.pregnancy_weeks = int(request.form['pregnancy_weeks'])
    user.height = float(request.form['height'])
    user.weight = float(request.form['weight'])
    
    db.session.commit()
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/diet_chart')
def diet_chart():
    if 'user_id' not in session:
        return redirect('/')
    user = User.query.get(session['user_id'])
    # Logic to generate personalized diet plan based on pregnancy stage
    return render_template('diet_chart.html', user=user)

@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')

@app.route('/mentor')
def mentor():
    return render_template('mentor.html')

@app.route('/fitness')
def fitness():
    return render_template('fitness.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run()