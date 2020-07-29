#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/29 9:20
# @Author : zhouzy_a
# @Version：V 0.1
# @File : user_id.py
# @desc : 用来生成用户唯一访问id


import uuid


USER_KEY = 'uid'
TEN_YEARS = 60*60*24*365*10


class UserIDMiddleware:
    """生成用户唯一id中间件，有效时长1年"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid