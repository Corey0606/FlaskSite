# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/11 11:57
@Author  : Corey
"""
from flask import Flask, request
from flask_restful import Api, Resource, marshal, fields, reqparse

app = Flask(__name__)
# restful接口方法
api = Api(app)

class UserApi(Resource):

    def get(self):
        return 'get restful api data'

    def post(self):
        return 'update restful api data'

    def delete(self):
        return 'delete restful api data '

api.add_resource(UserApi, '/users', endpoint='user')

if __name__ == '__main__':
    app.run()