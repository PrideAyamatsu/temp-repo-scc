from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    hospital_username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    vendor_username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    status = db.Column(db.String(20), default='current')  # 'current' or 'completed'

    hospital = db.relationship('User', foreign_keys=hospital_username, backref='hospital_orders')
    vendor = db.relationship('User', foreign_keys=vendor_username, backref='vendor_orders')