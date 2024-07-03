from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=36)])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=36)])
    user_type = SelectField('Type of Service', choices=[('hospital', 'Hospital'), ('vendor', 'Vendor'), ('delivery', 'Delivery')], validators=[DataRequired()])

class OrderForm(FlaskForm):
    item = StringField('Item', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    vendor = StringField('Vendor Username', validators=[DataRequired()])
