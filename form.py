from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TextAreaField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired,Email,Length,EqualTo

class resistration_form(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(min=3,max=12)])
    email=StringField('email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired()])
    confirm_password=PasswordField('confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Submit')

class login_forms(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(min=3,max=12)])
    password=PasswordField('password',validators=[DataRequired()])
    submit=SubmitField('login')

class update_form(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=3,max=12)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    picture=FileField('Update profile picture')
    submit=SubmitField('Submit')

class post_form(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    picture=FileField('Add Picture')
    submit=SubmitField("Post")