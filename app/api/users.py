from app.api import api
from app import db
from flask import jsonify, request, url_for
from app.models import User, Post
from app.api.errors import bad_request
from flask_login import login_user


# 用户登录校验
@api.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json() or {}
    if 'username' not in data:
        return bad_request('请输入用户名')
    if 'password' not in data:
        return bad_request('请输入用户名')
    user = User.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']):
        return bad_request('用户名或密码错误!')
    login_user(user)
    user.from_dict(data, new_user=False)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


# 根据 id 取得用户公开信息
@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    print('---------that----------')
    return jsonify(User.query.get_or_404(id).to_dict())


@api.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=1)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


# to_collection_dict()的最后两个参数是endpoint名称和id，
# id将在kwargs中作为一个额外关键字参数，然后在生成链接时将它传递给url_for()
@api.route('/users/<int:id>/followers', methods=['GET'])
def get_followers(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followers, page, per_page, 'api.get_followers', id=id)
    return jsonify(data)


@api.route('/users/<int:id>/followed', methods=['GET'])
def get_followed(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followed, page, per_page, 'api.get_followed', id=id)
    return jsonify(data)


# 创建一个新用户
@api.route('/users', methods=['POST'])
def create_user():
    print('--------1--------')
    # Flask提供request.get_json()方法从请求中提取JSON并将其作为Python结构返回
    data = request.get_json() or {}
    print(data)
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('此用户名已存在')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('此邮箱已注册过用户, 请使用不同邮箱注册新用户')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and User.query.filter_by(username=data['username']).first():
        return bad_request('此用户名已存在')
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('此邮箱已注册过用户, 请使用不同邮箱')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

