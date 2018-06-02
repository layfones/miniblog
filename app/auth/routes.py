from app.auth import auth
from app import db
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # 如果未找到用户或者密码错误, 给出提示并重定向回 login
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误!')
            return redirect(url_for('auth.login'))
        # 调用Flask-Login的login_user()函数
        # 将用户登录状态注册为已登录，user导航到任何未来的页面时，将user(用户实例)赋值给current_user变量。
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # @login_required装饰器保护的视图函数时
        # 将在这个重定向中包含一些额外的信息以便登录后的回转.
        # 使用Werkzeug的url_parse()函数解析，然后检查netloc属性是否被设置
        # 确定URL是相对的还是绝对的
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        # flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Sign In', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, about_me=' ')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)
