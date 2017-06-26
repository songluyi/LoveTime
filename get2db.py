# -*- coding: utf-8 -*-
# 2017/6/12 9:53
"""
-------------------------------------------------------------------------------
Function:   用来将QQ 信息标准化 导入mysql 数据库
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
from colorama import init, Fore, Back, Style
import re
# 改为sqllite3
import logging
logging.basicConfig(level=logging.INFO)
class get2db(object):
    # 调用一次 传递一个游标
    def __init__(self):
        # 这个我想通过爬虫来判断QQ的男女 这个样通过emgon的外部库
        self.boy_name = '一只特立独行的猪'
        self.girl_name= '一颗被拱了的白菜'
        return
    def connect_db(self):
        # 没发现这个用dict 可以传递现在用函数传递游标也行吧
        import sqlite3
        conn = sqlite3.connect('store.db')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS "msg" (
        "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        "qq_msg"  TEXT,
        "qq_user"  TEXT,
        "qq_time"  INTEGER
        );
        ''')
        return conn
    def get_path(self):
        import os
        current_path = os.path.abspath(os.path.join(os.path.dirname('get2db.py'), os.path.pardir))
        new_path = current_path + 'lovetime'+'\\' + 'msg'+'\\'
        FileList = []
        rootdir = new_path
        for root, subFolders, files in os.walk(rootdir):
            # 排除特定的子目录
            # if 'done' in subFolders:
            #     subFolders.remove('done')
            # 查找txt 聊天文件
            for f in files:
                if f.find('txt') != -1 :
                    FileList.append(os.path.join(root, f))

        for item in FileList:
            print(Fore.WHITE + '检测到您目录下有如下txt聊天文件 请确认是不是你要进行检测')
            print(item)
        return FileList
    def check_format(self, path_dict):
        for file in path_dict:
            file_count=0
            with open(file, 'r', encoding="utf8") as check_file:
                count=0
                error_tag=0
                for line in check_file:
                    count=count+1
                    if count==4:
                        if '消息分组' in line :
                            print(line)
                        else:
                            error_tag+=1
                    if count==6:
                        if '消息对象' in line:
                            print(line)
                            self.girl_name=line[9:]
                        else:
                            error_tag+=1
            if error_tag>0:
                print(Fore.RED +'该文本不符合导入要求，已经从列表中删除')
                del path_dict[file_count]
            else:
                print(Fore.GREEN +'检测完成 下一步生成数据库文件')
            file_count+=1
        return path_dict

    def check_title(self, string):
        result=re.findall('\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}', string)
        if result:
            return True
        else:
            return False

    def get_content(self,legal_path):
        data=[]
        for file in legal_path:
            with open(file, 'r', encoding='utf8') as qq_msg:
                db_content = {}
                msg_content = []
                # 现在目的就是为了解析 消息 导入到数据库
                for line in qq_msg.readlines()[8:]:

                    if get2db().check_title(line):
                        # 如果存在上一行信息封装好 那么本次运行就插入到数据库 或者自己再做一个字典
                        if db_content:
                            change_formate=(db_content['time'], db_content['content'], db_content['user'])
                            data.append(change_formate)
                            msg_content=[]
                            db_content={}
                        msg_time=re.findall('\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}',line)
                        msg_time=msg_time[0]
                        # 一般来讲 QQ的用户名20个字符就足够了
                        msg_user=re.findall('[\u4e00-\u9fa5]{1,20}',line)
                        if msg_user:
                            msg_user=msg_user[0]
                        else:
                            msg_user='用户名未查询到'
                        db_content['time']=msg_time
                        db_content['user']=msg_user
                    else:
                        msg_content.append(line)
                        qq_content=''.join(msg_content)
                        hh_content=qq_content.replace('\n', '')
                        db_content['content']=hh_content
        return data
    def insert_db(self,data):
        db = get2db().connect_db()
        cursor = db.cursor()
        insert_sql="INSERT INTO msg(qq_time,qq_msg,qq_user) VALUES (?, ?, ?)"
        select_sql="SELECT * FROM msg"
        cursor.execute(select_sql)
        check_result=cursor.fetchall()
        # 如果数据库为空才导入，不为空则不导入
        if check_result:
            print(Fore.YELLOW + '数据库中已经存在了需要检测的聊天记录,本次不会导入！')
        else:
            print(Fore.GREEN + '正在导入你的聊天数据，请稍后.....')
            cursor.executemany(insert_sql, data)
        db.commit()



if __name__=="__main__":
    msg=get2db()
    my_path=msg.get_path()
    my_content=msg.get_content(my_path)
    msg.insert_db(my_content)
