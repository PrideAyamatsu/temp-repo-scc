from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm, RegistrationForm, OrderForm
from models import db, User, Order
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['username'] = user.username
            session['user_type'] = user.user_type
            flash('Login successful!', 'success')
            
            # Redirect based on user_type
            if user.user_type == 'hospital':
                return redirect(url_for('hospital_dashboard'))
            elif user.user_type == 'vendor':
                return redirect(url_for('vendor_dashboard'))
            elif user.user_type == 'delivery':
                return redirect(url_for('delivery_dashboard'))
        else:
            flash('Login failed. Check your username and/or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password_hash=hashed_password, user_type=form.user_type.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/hospital_dashboard', methods=['GET', 'POST'])
def hospital_dashboard():
    if 'username' not in session or session['user_type'] != 'hospital':
        return redirect(url_for('login'))

    form = OrderForm()
    if form.validate_on_submit():
        vendor = User.query.filter_by(username=form.vendor.data).first()
        if vendor and vendor.user_type == 'vendor':
            new_order = Order(
                item=form.item.data,
                amount=form.amount.data,
                hospital_username=session['username'],
                vendor_username=form.vendor.data,
                status='current'
            )
            db.session.add(new_order)
            db.session.commit()
            flash('Order placed successfully!', 'success')
            return redirect(url_for('hospital_dashboard'))
        else:
            flash('Invalid vendor.', 'danger')

    current_orders = Order.query.filter_by(hospital_username=session['username'], status='current').all()
    past_orders = Order.query.filter_by(hospital_username=session['username'], status='completed').all()

    return render_template('hospital_dashboard.html', form=form, current_orders=current_orders, past_orders=past_orders)

@app.route('/vendor_dashboard')
def vendor_dashboard():
    if 'username' not in session or session['user_type'] != 'vendor':
        return redirect(url_for('login'))

    orders = Order.query.filter_by(vendor_username=session['username'], status='current').all()
    return render_template('vendor_dashboard.html', orders=orders)

@app.route('/delivery_dashboard')
def delivery_dashboard():
    if 'username' not in session or session['user_type'] != 'delivery':
        return redirect(url_for('login'))
    return render_template('delivery_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
