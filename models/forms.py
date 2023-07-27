from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, validators
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    nombre = StringField(label='Name', validators=[DataRequired(message="Data required")],  render_kw={"placeholder": "Name"})
    apellidos = StringField(label='Last Name', validators=[DataRequired(message="Data required"), validators.Length(min=3,max=15)], render_kw={"placeholder": "Last Name"})
    email = EmailField(label='Email', validators=[DataRequired(message="Data required"), validators.Email(message="Introduce a valid email")], render_kw={"placeholder": "Email"})
    password = PasswordField(label='Password', validators=[DataRequired(message="Data required"),  validators.EqualTo("confirmar_password", message="Passwords doesn't match")], render_kw={"placeholder": "Password"})
    confirmar_password = PasswordField(label='Confirm Password', validators=[DataRequired(message="Data required"), validators.length(min=8, message="Password too short")], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField(label="Register")

class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(message="Data required"), validators.Email(message="Please, introduce a valid mail")], render_kw={"placeholder": "Email"})
    password = PasswordField(label='Password',  validators=[DataRequired(message="Data required")], render_kw={"placeholder": "Password"})
    submit = SubmitField(label="Sign in")

class ResetPassword(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired(message="Data required"),  validators.EqualTo("confirmar_password", message="Passwords doesn't match")], render_kw={"placeholder": "Password"})
    confirmar_password = PasswordField(label='Confirm Password', validators=[DataRequired(message="Data required"), validators.length(min=8, message="Too short")], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField(label="Change Password")

class ForgotPassword(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(message="Data required"), validators.Email(message="Please, introduce a valid mail")], render_kw={"placeholder": "Email"})
    submit = SubmitField(label="Change Password")

