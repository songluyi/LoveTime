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
    def __init__(self, error_code='404', msg='a small beauty bug'):
        # Exception 继承后我发现 这个msg 才不会被pycharm 标黄
        super(LoveError, self).__init__(error_code, msg)
        self.error_code = error_code
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class ValueError(LoveError):
    def __init__(self, value_code='006', msg='program can not run as there is value error'):
        super(ValueError, self).__init__(value_code, msg)


class FileError(LoveError):
    def __init__(self, file_code='007', msg="please input your msg file"):
        super(FileError, self).__init__(error_code=file_code, msg=msg)
