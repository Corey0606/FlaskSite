# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/6 17:46
@Author  : Corey
"""
import requests
import json

account = {"username": "corey", "password": "fcf781jkjk"}
# result = requests.post("http://www.coreychen.cn/api/login", data=account)
result = requests.post("http://127.0.0.1:5000/api/login", data=account)
token = json.loads(result.text)["access_token"]

#### project
# d = {'name': '近期项目预览', 'icon': 'fa-windows', 'weight': 10,
#      'introduce': "展示2020年交付项目开发的页面。语言：python 页面：基于PYQT5",
#      'article_url': 0}
#
# result = requests.post("http://www.coreychen.cn/api/project", data=json.dumps(d),
#                        headers={"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"})
# print("code", result.status_code)
# print("content", json.loads(result.text)["message"])

# {'topic':str,'picture_url':str,'article_url':1,'weight':0,'introduce':str,'link_project':0}

##### article
# post_dict = {'topic': "线上crm报价管理系统", 'picture_url': "images/pic01.jpg", 'article_url': 1, 'weight': 1,
#              'introduce': "公司内部全员使用的报价权限系统，与公司钉钉交互。主要用途生成客户报价单。开发语言：python 后端框架:Django2.1 前端:Html5,Js,Jquery 数据库:Sqlite 服务器:windows server2016", 'link_project': 4}
# result = requests.post("http://127.0.0.1:5000/api/article", data=json.dumps(post_dict),
#                       headers={"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"})
# print("code", result.status_code)
# print("content", json.loads(result.text)["message"])

###content
with open(r"C:\Users\liping\Desktop\md\项目\报价软件\报价软件.md", "r", encoding="utf-8") as f:
    content = f.read().strip()

d = {"id": 5, "content_md": content}
result = requests.put("http://127.0.0.1:5000/api/content", data=json.dumps(d),
                      headers={"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"})
print("code", result.status_code)
print("content", json.loads(result.text)["message"])

## content
