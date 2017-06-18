# -*- coding: utf-8 -*-
# 2017/6/14 21:50
"""
-------------------------------------------------------------------------------
Function:   在这里监控 数据
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
# 引入数据库游标函数
from colorama import init, Fore, Back, Style
from get2db import get2db
class moniter_platform(object):
    def __init__(self):
        self.db_result=[]

        return

    def visual_time(self):

        check_result=self.get_field()
        index_result=dict()
        hour_result=dict()
        for i in check_result:
            # 开始桶排序 取前10字节 的日期
            index_day=str(i)[0:10]
            index_hour=str(i)[11:13]
            count=index_result.get(index_day,0)
            hour_count=hour_result.get(index_hour,0)
            if int(count)>0:
                middle_num=index_result[index_day]+1
                index_result[index_day] =middle_num
            else:
                index_result[index_day] = 1
            if int(hour_count)>0:
                middle_hour=hour_result[index_hour]+1
                hour_result[index_hour]=middle_hour
            else:
                hour_result[index_hour]=1
        day_list=sorted(moniter_platform().dict2list(index_result), key=lambda x:x[1], reverse=True)
        hour_list=sorted(moniter_platform().dict2list(hour_result), key=lambda x:x[1], reverse=True)

        return [day_list,hour_list]

    def dict2list(self,dic):
        ''' 将字典转化为列表 '''
        keys = dic.keys()
        vals = dic.values()
        lst = [(key, val) for key, val in zip(keys, vals)]
        return lst
    def turn_tuplelist(self,dic1,dic2):
        new_dict=[]
        for i in range(0, len(dic1)):
            new_dict.append((dic1[i],dic2[i]))
        return new_dict
    # 获取数据库中字段，默认为获取时间
    def get_field(self, num=3):
        back_result = []
        # 如果db_result为空 就到数据区中取值 否则就用平时已经存储过的值
        if not self.db_result:
            db=get2db().connect_db()
            cursor = db.cursor()
            all_sql='select * from id'
            cursor.execute(all_sql)
            check_result = cursor.fetchall()
            self.db_result=check_result

            for i in check_result:
                back_result.append(i[num])
        else:
            for i in self.db_result:
                back_result.append(i[num])
        return back_result
    def reply_rate(self):
        reply_data=self.turn_tuplelist(self.get_field(2),self.get_field())
        first_strike_up=reply_data[0][0]
        gap_list=[]
        for i in range(0,len(reply_data)-1):
            if str(reply_data[i][0]) != str(reply_data[i+1][0]):
                gap_time=reply_data[i+1][1] - reply_data[i][1]
                gap_list.append(gap_time)
        sum_time=gap_list[0]
        for i in gap_list:
            sum_time=sum_time+i
        all_avg_time=sum_time/len(gap_list)
        print(Fore.GREEN+'平均回复'+'【'+first_strike_up+ '】'+'的时间是：'+str(all_avg_time))
        return
moniter=moniter_platform()

day_index,hour_index=moniter.visual_time()

s=moniter.turn_tuplelist(moniter.get_field(2),moniter.get_field())
# print(s)
moniter.reply_rate()