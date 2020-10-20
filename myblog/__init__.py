from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app=Flask(__name__)
app.secret_key="hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shivam.db'
db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view="login"
login_manager.login_message_category="info"

from myblog import routes

