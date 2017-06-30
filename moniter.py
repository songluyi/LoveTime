# -*- coding: utf-8 -*-
# 2017/6/14 21:50
"""
-------------------------------------------------------------------------------
Function:   monitor data in this place
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
import datetime
import logging
logging.basicConfig(level=logging.INFO)
def log(msg):
    logging.info(str(msg))
from get2db import get2db
class moniter_platform(object):

    def __init__(self):
        self.db_result=self.get_db_reslt()
        self.first_strike_up=''
        self.sec_strike_up=''
        self.history_name=[]
        self.chat_his=[]# 聊天历史年份
        self.year_time=2# 默认时长两年
        self.time_gap=[]
        self.sql='select * from msg'

    def get_db_reslt(self):
        sql='select * from msg'
        db=get2db().connect_db()
        cursor = db.cursor()
        cursor.execute(sql)
        check_result = cursor.fetchall()
        return check_result

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

    def get_field(self, num=3, time_limit=None, *condition):
        back_result = []
        sql_condition=condition
        # 存在condition where 语句 就重新执行sql 否则就用统一的
        if sql_condition:
            sql_plus='where'+sql_condition[0]+'='+sql_condition[1]
            all_sql = self.sql + sql_plus
            db=get2db().connect_db()
            cursor = db.cursor()
            cursor.execute(all_sql)
            check_result = cursor.fetchall()
        else:
            sql_plus=''
            check_result=self.db_result

        # 如果db_result为空 就到数据区中取值 否则就用平时已经存储过的值
        # if not self.db_result:
        # db=get2db().connect_db()
        # cursor = db.cursor()
        # # all_sql='select * from msg'
        # cursor.execute(all_sql)
        # check_result = cursor.fetchall()

        for i in check_result:
            if not time_limit:
                back_result.append(i[num])
            else:
                tail_time=datetime.datetime.strptime(time_limit[0],'%Y-%m-%d')
                header_time=datetime.datetime.strptime(time_limit[1],'%Y-%m-%d')
                compare_time=datetime.datetime.strptime(i[3],'%Y-%m-%d %H:%M:%S')
                if compare_time <= header_time and compare_time >= tail_time:
                     back_result.append(i[num])
        # else:
        #     for i in self.db_result:
        #         if not time_limit:
        #             back_result.append(i[num])
        #         else:
        #             tail_time=datetime.datetime.strptime(time_limit[0],'%Y-%m-%d')
        #             header_time=datetime.datetime.strptime(time_limit[1],'%Y-%m-%d')
        #             compare_time=datetime.datetime.strptime(i[3],'%Y-%m-%d %H:%M:%S')
        #             if compare_time <= header_time and compare_time >= tail_time:
        #                  back_result.append(i[num])
        # print(back_result)
        return back_result

    # 获取聊天的年份 方便对回复速率进行年份间的评估
    def get_chat_his(self):
        time_data=self.get_field(3)
        chat_his=[]
        tail_flag=header_flag=False
        count=0
        for i in time_data:
            count+=1
            if count==1 and int(str(i)[5:7])<7:
                print(int(str(i)[5:7]))
                tail_flag=True
            if count==len(time_data) and int(str(i)[5:7])>5:
                header_flag=True
            if str(i)[0:4] not in chat_his:
                chat_his.append(str(i)[0:4])
        # 第一个布尔类型表示最开始年份是否有半年之久
        # 第二个布尔类型表示后续年份超过六个月
        chat_his.append(tail_flag)
        chat_his.append(header_flag)
        self.chat_his=chat_his
        log(chat_his)
        return chat_his

    def get_first_strike(self):
        reply_data = self.turn_tuplelist(self.get_field(2), self.get_field(3))
        self.first_strike_up = reply_data[0][0]
        return self.first_strike_up


    def reply_rate(self,interval_time=None):
        reply_data=self.turn_tuplelist(self.get_field(2,interval_time),self.get_field(3,interval_time))
        # 第一次打招呼的人
        # print(reply_data)
        # first_strike_up=reply_data[0][0]
        # self.first_strike_up=first_strike_up
        first_strike_up=self.get_first_strike()
        first_gap_list=[]
        sec_gap_list=[]

        for i in range(0,len(reply_data)-1):
            # 如果两条中的后一条不是最先打招呼的那人发的
            if first_strike_up != str(reply_data[i+1][0]) :
                self.sec_strike_up=str(reply_data[i+1][0])
                # 对 研究记录对象的 曾用名 进行统计
                # print(first_strike_up)
                filter_name=str(reply_data[i+1][0]).replace('系统消息','').replace('用户名未查询到','')
                if filter_name not in self.history_name and filter_name !='':
                    self.history_name.append(str(reply_data[i+1][0]))
                # 由于改用sqllite 导致这里时间格式需要再脚本计算修改
                gap2_time=datetime.datetime.strptime(reply_data[i+1][1],'%Y-%m-%d %H:%M:%S')
                gap1_time=datetime.datetime.strptime(reply_data[i][1],'%Y-%m-%d %H:%M:%S')
                first_gap_time=gap2_time - gap1_time
                first_gap_list.append(first_gap_time)
            elif first_strike_up==str(reply_data[i+1][0]):
                gap2_time=datetime.datetime.strptime(reply_data[i+1][1],'%Y-%m-%d %H:%M:%S')
                gap1_time=datetime.datetime.strptime(reply_data[i][1],'%Y-%m-%d %H:%M:%S')
                sec_gap_time= gap2_time - gap1_time

                sec_gap_list.append(sec_gap_time)
        # 这个数据格式还是满奇特的
        first_sum_time=datetime.timedelta(0, 0)
        sec_sum_time=datetime.timedelta(0, 0)
        for i in first_gap_list:
            first_sum_time=first_sum_time+i
        for j in sec_gap_list:
            sec_sum_time=sec_sum_time+j
        first_avg_time=first_sum_time/len(first_gap_list)
        sec_avg_time=sec_sum_time/len(sec_gap_list)

        if int(interval_time[1][:4])-int(interval_time[0][:4])==1:
            time_axis=interval_time[0][:4]+'下半年'
        elif int(interval_time[1][:4])-int(interval_time[0][:4])==0:
            time_axis=interval_time[0][:4]+'上半年'
        else:
            time_axis='Wrong'
        print(self.history_name)
        print(time_axis)
        print(Fore.GREEN + '平均回复' + '【' + self.first_strike_up + '】' + '的时间是：' + str(first_avg_time))
        print(Fore.GREEN + '平均回复' + '【' + self.sec_strike_up + '】' + '的时间是：' + str(sec_avg_time))
        return [time_axis, first_strike_up, sec_avg_time]
    def get_time_gap(self):
        if not self.chat_his:
            self.get_chat_his()
        self.year_time=len(self.chat_his[:-2])

        for year in self.chat_his[:-2]:
            self.time_gap.append(str(year)+'-01-01')
            self.time_gap.append(str(year)+'-06-01')
        # 若存在最初日期大于六月份
        log(self.chat_his)
        if not self.chat_his[-2]:
            self.time_gap=self.time_gap[1:]
        if not self.chat_his[-1]:
            self.time_gap=self.time_gap[:-1]

        log('your time_gap %s'%self.time_gap)
        return self.time_gap




# 这些复杂的函数 到时还是写一个unittest
moniter=moniter_platform()
count=0
moniter.get_time_gap()
print(moniter.time_gap[:-1])
for gap in moniter.time_gap[:-1]:
    # print(moniter.time_gap[count + 1])
    small_gap=[moniter.time_gap[count], moniter.time_gap[count+1]]
    moniter.reply_rate(small_gap)
    count += 1