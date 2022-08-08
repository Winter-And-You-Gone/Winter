import random

from app import app, db
from flask import current_app, render_template, flash, redirect, url_for, \
    request
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/favicon.ico')  # 设置icon
def favicon():
    return current_app.send_static_file('favicon.ico')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
@login_required
def index():
    user = {}
    posts = []
    return render_template('index.html', title='我的', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    # 对表格数据进行验证
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('无效的用户名或密码')
            
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # 此时的next_page记录的是跳转至登录页面是的地址
        next_page = request.args.get('next')
        # 如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # 综上，登录后要么重定向至跳转前的页面，要么跳转至首页
        return redirect(next_page)
    return render_template('login.html', title='登录', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    img_url='../static/images/head.jpg',
                    about_me='其人甚懒，无所留也...')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    form = EditProfileForm()
    form.img_url.data = current_user.img_url
    user = User.query.filter_by(username=username).first_or_404()
    posts = [{'author': user, 'body': '测试Post #1号'},
             {'author': user, 'body': '测试Post #2号'}]
    
    return render_template('user.html', user=user, posts=posts, form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        f = request.files.get('img_file')
        rd = random.randint(10000, 99999)
        basedir = '/static/images' + '/' + form.username.data
        f_name = str(rd) + f.filename
        f_path = './app' + basedir + '/' + f_name
        f.save(f_path)
        f_path = '..' + basedir + '/' + f_name
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.img_url = f_path
        db.session.commit()
        flash('个人资料修改成功')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.img_url.data = current_user.img_url
        print(form.img_url.data)  # 在点后加啥就是啥标签，例如label，input，data(数据的值)
    return render_template('edit_profile.html', title='个人资料', form=form)
