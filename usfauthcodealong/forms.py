from wtforms import Form, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm



class SignUp(FlaskForm):
    username = StringField('Username:', validators=[InputRequired()])
    password = StringField('Password:', validators=[InputRequired()])
    email = StringField('Email Address:', validators=[InputRequired()])
    first_name = StringField('First Name:', validators=[InputRequired()])
    last_name = StringField('Last Name:', validators=[InputRequired()])
    submit = SubmitField('Submit')


class LogIn(FlaskForm):
    username = StringField('Username:', validators=[InputRequired()])
    password = StringField('Password:', validators=[InputRequired()])
    submit = SubmitField('Log In')

class FeedbackForm(FlaskForm):
    title = StringField('Title:', validators=[InputRequired()])
    content = TextAreaField('Content:', validators=[InputRequired()])
    submit = SubmitField('Submit')
