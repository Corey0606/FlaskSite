# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/6 17:46
@Author  : Corey
"""
import requests
import json

account = {"username": "corey", "password": "fcf781jkjk"}
result = requests.post("http://127.0.0.1:5000/api/login", data=account)
token = json.loads(result.text)["access_token"]

# project
# d = {'name': '我的主站搭建', 'icon': 'fa-newspaper-o', 'weight': 10,
#      'introduce': "欢迎来到Corey的个人主站，本站点原生模板源自HTML5 UP，是一个Jquery的自适应模板。后加工基于Flask，服务器环境为centos+nginx+uwsgi。",
#      'article_url': 0}
# result = requests.post("http://127.0.0.1:5000/api/project", data=json.dumps(d), headers={"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"})
# print("code", result.status_code)
# print("content", json.loads(result.text)["message"])

# article
with open(r"C:\Users\liping\Desktop\learn\test.md", "r", encoding="utf-8") as f:
    content = f.read().strip()
d = {"id": 1, "content_md": content}
result = requests.put("http://127.0.0.1:5000/api/content", data=json.dumps(d),
                       headers={"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"})
print("code", result.status_code)
print("content", json.loads(result.text)["message"])

