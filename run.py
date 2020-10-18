from flask import Flask,render_template,flash,redirect,url_for,request
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from form import *
from flask_login import LoginManager,UserMixin,login_user,current_user,login_required,logout_user
from passlib.hash import pbkdf2_sha256
from PIL import Image
import os
import secrets




app=Flask(__name__)
app.secret_key="hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shivam.db'
db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view="login"
login_manager.login_message_category="info"


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path,'static/images',picture_fn)
    output_size=(100,100)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_fn)
    i.save(picture_path)
    return picture_fn


def save_picture_post(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path,'static/post_images',picture_fn)
    output_size=(675,404)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_fn)
    i.save(picture_path)
    return picture_fn


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


@app.route("/")
@login_required
def main():
    forms=login_forms()
    page=request.args.get('page',1,type=int)
    post=posts.query.order_by(posts.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template("main.html",post=post,forms=forms)


@app.route("/resister",methods=['GET','POST'])
def resister():
    form=resistration_form()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=form.password.data
        hashed_password=pbkdf2_sha256.hash(password)
        user_object=user.query.filter_by(username=username).first()
        if user_object:
            flash("account already exist! please try something new")
            return redirect(url_for('resister',forms=forms))
        entry=user(username=username,email=email,password=hashed_password)
        db.session.add(entry)
        db.session.commit()
        flash("account is created please submit credentials")
        return redirect(url_for('login'))

    return render_template("re.html",form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    forms=login_forms()
    if forms.validate_on_submit():
        username_entered=forms.username.data
        password_entered=forms.password.data
        user_object=user.query.filter_by(username=username_entered).first()
        if user_object and pbkdf2_sha256.verify(password_entered,user_object.password):
            login_user(user_object)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else  redirect(url_for('main'))
        else:
            flash("Incorrect username or password")
            return render_template("login.html",forms=forms)
    else:
        return render_template('login.html',forms=forms)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route("/profile",methods=['GET','POST'])
@login_required
def profile():
    form=update_form()
    if form.validate_on_submit():
        if form.picture.data:
            picture_fn=save_picture(form.picture.data)
            current_user.image_file=picture_fn
        data=form.username.data
        current_user.username=form.username.data
        current_user.email=form.email.data
        try:
            db.session.commit()    
            return redirect(url_for('profile'))
        except Exception:
            message="form is invalid"
            return redirect(url_for('profile',message=message))
    elif request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for('static',filename='images/'+current_user.image_file)
    return render_template('profile.html',image_file=image_file,form=form)


@app.route("/post",methods=["GET","POST"])
def post():
    form=post_form()
    if form.validate_on_submit():
        if form.picture.data:
            picture_fn=save_picture_post(form.picture.data)
            picture=picture_fn
        flash("Post successfully!")
        title=form.title.data
        title=title.title()
        content=form.content.data
        content=content.title()
        entry=posts(title=title,content=content,author=current_user,picture=picture)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template("post.html",form=form)

@app.route("/userposts/<int:id>")
def userposts(id):
    post=posts.query.get_or_404(id)
    return render_template('userposts.html',post=post)

@app.route("/userposts/<int:id>/update",methods=['GET','POST'])
@login_required
def update_post(id):
    post=posts.query.get_or_404(id)
    if post.author!=current_user:
        abort(403)
    form=post_form()
    if form.validate_on_submit():
        if form.picture.data:
            picture=save_picture_post(form.picture.data)
            post.picture=picture
        title=form.title.data
        title=title.title()
        post.title=title
        content=form.content.data
        content=content.title()
        post.content=content
        db.session.commit()
        return redirect(url_for('userposts',id=post.id))
    elif request.method=="GET":
        form.title.data=post.title
        form.content.data=post.content
    return render_template('post.html',form=form)

@app.route("/userposts/<int:id>/delete",methods=["GET","POST"])
@login_required
def delete_post(id):
    post=posts.query.get_or_404(id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main'))
    
@app.route("/login_form")
def login_form():
    form=resistration_form()
    return render_template("login_form.html",form=form)


if __name__=="__main__":
    app.run(debug=True)