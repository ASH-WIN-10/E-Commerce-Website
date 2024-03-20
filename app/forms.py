from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login", validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register", validators=[DataRequired()])

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError("This email is already registered.")
        
class AddItemForm(FlaskForm):
    item_name = StringField("Item name", validators=[DataRequired()])
    item_description = TextAreaField("Item description", validators=[DataRequired(), Length(max=512)])
    price = IntegerField("Price", validators=[DataRequired()])
    img_url = URLField("Item image")
    submit = SubmitField("Add")