# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/11 12:00
@Author  : Corey
"""
import time

from flask import Flask, jsonify, url_for, request, g
from flask_restful import Api, abort
# flask SQLAlchemy模块，实现ORM框架操作
from flask_sqlalchemy import SQLAlchemy
# flask自带httpauth模块，BasicAuth和tokenAuth子模块
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
# 密码散列加密模块
from passlib.apps import custom_app_context as pwd_context
# jwt-- token生成模块
import jwt

# werkzeug密码加密模块，有兴趣的可以自行了解
# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)

# 关于flask SQLAlchemy实现ORM框架操作的一些基础配置
app.config['SECRET_KEY'] = 'dqwecf29vbneuirjnf2i3n0f2i302n'
# 数据库连接信息配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# 是否自动提交sql执行
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 是否显示修改回执
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# SQLAlchemy实例化
db = SQLAlchemy(app)
# 引入基础认证、token认证模块
auth = HTTPBasicAuth()
token_m = HTTPTokenAuth()


class User(db.Model):
    # 表名
    __tablename__ = 'users'
    # 表字段名对应赋值属性
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    # print(id, username, password_hash)

    # def __init__(self, username, password_hash):
    #     self.username = username
    #     self.password_hash = password_hash

    # 生成密码散列方法
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # 校验密码方法
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # 生成token方法
    def generate_auth_token(self):
        # print(time.time())
        print("self id ", self.id)
        print(self.username)
        print(self.password_hash)
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + 600},
            app.config['SECRET_KEY'], algorithm='HS256')

    # 校验token方法
    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
            print(data)
        except Exception as e:
            print(e)
            return False
        user = User.query.get(data['id'])
        print("user", user)
        return user


# 在初次请求时，进行数据的表创建
# 实际开发中，此处一般会在数据库中已经完成，研发人员只需要关注表结构，并进行对应的字段操作即可
@app.before_first_request
def create_db():
    # 删除
    db.drop_all()
    # 创建
    db.create_all()


# 根据密码登录认证装饰器进行请求携带的密码信息校验
@auth.verify_password
def verify_password(username_or_token, password):
    user = User.query.filter_by(username=username_or_token).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


# 根据token登录认证装饰器进行请求携带的token校验
@token_m.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    g.user = user
    if not user:
        return False
    return True


# 获取用户访问信息，并根据判断信息，添加新用户
@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        print('existing user')
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


# 查询指定用户方法
@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


# 查询所有用户方法
@app.route('/api/users', methods=['GET'])
def get_all_user():
    users = User.query.all()
    if not users:
        abort(400)
    return jsonify(["{0}, {1}".format(user.username, user.password_hash) for user in users])


# 基于密码生成token方法
@app.route('/api/token')
# 密码登录验证装饰器
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


# token认证方法
@app.route('/api/resource')
# token登录验证装饰器
@token_m.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.errorhandler(400)
def error(e):
    print(e)
    return '错误请求', 400


if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
