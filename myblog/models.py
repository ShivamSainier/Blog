from myblog import db,login_manager
from datetime import date
from flask_login import UserMixin


@login_manager.user_loader
def load(id):
    return user.query.get(id)


class user(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    username=db.Column(db.String(120),nullable=False,unique=True)
    email=db.Column(db.String(120),nullable=False)
    password=db.Column(db.String(120),nullable=False)
    image_file=db.Column(db.String(120),nullable=False,default='default.jpg')
    post=db.relationship('posts',backref='author',lazy=True)
    
    def __repr__(self):
        return f"user('{self.username}','{self.email}','{self.image_file}','{self.password}')"

class posts(db.Model):
    date=date.today()
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.Text,nullable=False)
    content=db.Column(db.Text,nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=date)
    picture=db.Column(db.String(120),nullable=False,default='default.jpg')
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=True)
    def __repr__(self):
        return f"user('{self.title}','{self.date_posted}'),{self.picture}')"