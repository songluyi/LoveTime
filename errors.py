# -*- coding: utf-8 -*-
# 2017/6/24 18:09
"""
-------------------------------------------------------------------------------
Function:   封装error信息
Version:    1.0
Author:     SLY
Contact:    slysly759@gmail.com 

code is far away from bugs with the god Animal protecting
               ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
                  
-------------------------------------------------------------------------------
"""
'''
error definition

'''
# 父类继承以及使用并未真正掌握
class LoveError(Exception):
    def __init__(self, error, data='', msg=''):
        # Exception 继承后我发现 这个msg 才不会被pycharm 标黄
        super(LoveError,self).__init__(msg)
        self.data=error
        self.error=data
        self.msg=msg

class ValueError(LoveError):
    def __init__(self, field, msg):
        super(ValueError,self).__init__('program can not run as there is value error', field, msg)

