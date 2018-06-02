from app.api import api
from app.models import Post, Comment
from app import db
from flask import jsonify, request, url_for, redirect
from app.api.errors import bad_request


@api.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    print('---------this----------')
    return jsonify(Post.query.get_or_404(id).to_dict())


@api.route('/posts', methods=['GET'])
def get_posts():
    print('---------that----------')
    page = request.args.get('page', 1, type=1)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    posts = Post.to_collection_dict(Post.query.order_by(Post.timestamp.desc()), page, per_page, 'api.get_posts')
    return jsonify(posts)


@api.route('/posts', methods=['POST'])
def new_post():
    # Flask提供request.get_json()方法从请求中提取JSON并将其作为Python结构返回
    data = request.get_json() or {}
    print(data)
    if 'body' not in data or 'user_id' not in data:
        return bad_request('must include body fields')
    post = Post()
    post.from_dict(data, new_post=True)
    # print('000000000000000000000000')
    # print(post)
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response


@api.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get_or_404(id)
    data = request.get_json() or {}
    post.from_dict(data, new_post=False)
    db.session.commit()
    return jsonify(post.to_dict())


@api.route('/posts/<int:id>/comments', methods=['GET'])
def get_comments(id):
    print('---------this----------')
    post = Post.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(post.comments.order_by(Comment.timestamp.desc()), page, per_page, 'api.get_comments', id=id)
    return jsonify(data)


@api.route('/posts/<int:id>', methods=['POST'])
def new_comment(id):
    data = request.get_json() or {}
    print(data)
    if 'body' not in data or 'author_id' not in data:
        return bad_request('must include body fields')
    comment = Comment()
    comment.from_dict(data)
    comment.post_id = id
    # print('000000000000000000000000')
    # print(post)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('api.get_comments', id=comment.post_id))
