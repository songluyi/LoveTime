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
'''
这两兆的文件处理起来太慢了，每次都是从新使用游标读取 在效率上应该可以优化
这方面需要加强
'''
from colorama import init, Fore, Back, Style
from collections import Counter
import datetime
from jieba import analyse
# 效率的事情稍 后来转么进行实现 特别是规范化的问题
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
# 生成词云图
import jieba
import logging
import os

LOG_FILENAME_NOTE = "./log/log.txt"
logging.basicConfig(filename=LOG_FILENAME_NOTE, level=logging.INFO)


def log(msg):
    logging.info(str(msg))


from get2db import get2db


class moniter_platform(object):
    def __init__(self):
        self.db_result = self.get_db_reslt()
        self.first_strike_up = ''
        self.sec_strike_up = ''
        self.history_name = []
        self.chat_his = []  # 聊天历史年份
        self.year_time = 2  # 默认时长两年
        self.time_gap = []
        self.sql = 'select * from msg'
        self.count_word = {}

    def get_db_reslt(self):
        sql = 'select * from msg'
        db = get2db().connect_db()
        cursor = db.cursor()
        cursor.execute(sql)
        check_result = cursor.fetchall()
        return check_result

    def visual_time(self):
        check_result = self.get_field()
        index_result = dict()
        hour_result = dict()
        for i in check_result:
            # 开始桶排序 取前10字节 的日期
            index_day = str(i)[0:10]
            index_hour = str(i)[11:13]
            count = index_result.get(index_day, 0)
            hour_count = hour_result.get(index_hour, 0)
            if int(count) > 0:
                middle_num = index_result[index_day] + 1
                index_result[index_day] = middle_num
            else:
                index_result[index_day] = 1
            if int(hour_count) > 0:
                middle_hour = hour_result[index_hour] + 1
                hour_result[index_hour] = middle_hour
            else:
                hour_result[index_hour] = 1
        day_list = sorted(self.dict2list(index_result), key=lambda x: x[1], reverse=True)
        hour_list = sorted(self.dict2list(hour_result), key=lambda x: x[1], reverse=True)
        new_day_list=self.dict_tuple_2_json(day_list)
        new_hour_list = self.dict_tuple_2_json(hour_list)
        # 新建转换
        self.json2file(new_day_list,'day.json')
        self.json2file(new_hour_list, 'hour.json')
        return [new_day_list, new_hour_list]
    '''
    该方法主要用于 将字典 转换为js 可以识别的 json txt
    但是 后续 还需要润色
    '''
    def dict_tuple_2_json(self,dict_tuple):
        back_dict={}
        x_data=[]
        y_data=[]
        for i in dict_tuple:
            # 注意： 这里有可能前面字符串截取有问题
            x_data.append(str(i[0]).replace(':',''))
            y_data.append(i[1])
        back_dict['x_data']=x_data
        back_dict['y_data']=y_data
        return back_dict

    def dict2list(self, dic):
        ''' 将字典转化为列表 '''
        keys = dic.keys()
        vals = dic.values()
        lst = [(key, val) for key, val in zip(keys, vals)]
        return lst

    def turn_tuplelist(self, dic1, dic2):
        new_dict = []
        for i in range(0, len(dic1)):
            new_dict.append((dic1[i], dic2[i]))
        return new_dict

    # 获取数据库中字段，默认为获取时间
    # 仅接受 一个condition
    def get_field(self, num=3, time_limit=None, *condition):
        back_result = []
        sql_condition = condition
        # 存在condition where 语句 就重新执行sql 否则就用统一的
        if sql_condition:
            sql_plus = ' where ' + str(sql_condition[0]) + '=' + "'" + str(sql_condition[1]) + "'"
            all_sql = self.sql + sql_plus
            db = get2db().connect_db()
            cursor = db.cursor()
            log(all_sql)
            cursor.execute(all_sql)
            check_result = cursor.fetchall()
        else:
            sql_plus = ''
            check_result = self.db_result

        # 如果db_result为空 就到数据区中取值 否则就用平时已经存储过的值

        for i in check_result:
            if not time_limit:
                back_result.append(i[num])
            else:
                tail_time = datetime.datetime.strptime(time_limit[0], '%Y-%m-%d')
                header_time = datetime.datetime.strptime(time_limit[1], '%Y-%m-%d')
                compare_time = datetime.datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S')
                if compare_time <= header_time and compare_time >= tail_time:
                    back_result.append(i[num])
        return back_result

    # 获取聊天的年份 方便对回复速率进行年份间的评估
    def get_chat_his(self):
        time_data = self.get_field(3)
        chat_his = []
        tail_flag = header_flag = False
        count = 0
        for i in time_data:
            count += 1
            if count == 1 and int(str(i)[5:7]) < 7:
                print(int(str(i)[5:7]))
                tail_flag = True
            if count == len(time_data) and int(str(i)[5:7]) > 5:
                header_flag = True
            if str(i)[0:4] not in chat_his:
                chat_his.append(str(i)[0:4])
        # 第一个布尔类型表示最开始年份是否有半年之久
        # 第二个布尔类型表示后续年份超过六个月
        chat_his.append(tail_flag)
        chat_his.append(header_flag)
        self.chat_his = chat_his
        log(chat_his)
        return chat_his

    def get_first_strike(self):
        reply_data = self.turn_tuplelist(self.get_field(2), self.get_field(3))
        self.first_strike_up = reply_data[0][0]
        return self.first_strike_up

    def reply_rate(self, interval_time=None):
        reply_data = self.turn_tuplelist(self.get_field(2, interval_time), self.get_field(3, interval_time))
        # 第一次打招呼的人
        # print(reply_data)
        # first_strike_up=reply_data[0][0]
        # self.first_strike_up=first_strike_up
        first_strike_up = self.get_first_strike()
        first_gap_list = []
        sec_gap_list = []

        for i in range(0, len(reply_data) - 1):
            # 如果两条中的后一条不是最先打招呼的那人发的
            if first_strike_up != str(reply_data[i + 1][0]):
                self.sec_strike_up = str(reply_data[i + 1][0])
                # 对 研究记录对象的 曾用名 进行统计
                # print(first_strike_up)
                filter_name = str(reply_data[i + 1][0]).replace('系统消息', '').replace('用户名未查询到', '')
                if filter_name not in self.history_name and filter_name != '':
                    self.history_name.append(str(reply_data[i + 1][0]))
                # 由于改用sqllite 导致这里时间格式需要再脚本计算修改
                gap2_time = datetime.datetime.strptime(reply_data[i + 1][1], '%Y-%m-%d %H:%M:%S')
                gap1_time = datetime.datetime.strptime(reply_data[i][1], '%Y-%m-%d %H:%M:%S')
                first_gap_time = gap2_time - gap1_time
                first_gap_list.append(first_gap_time)
            elif first_strike_up == str(reply_data[i + 1][0]):
                gap2_time = datetime.datetime.strptime(reply_data[i + 1][1], '%Y-%m-%d %H:%M:%S')
                gap1_time = datetime.datetime.strptime(reply_data[i][1], '%Y-%m-%d %H:%M:%S')
                sec_gap_time = gap2_time - gap1_time

                sec_gap_list.append(sec_gap_time)
        # 这个数据格式还是满奇特的
        first_sum_time = datetime.timedelta(0, 0)
        sec_sum_time = datetime.timedelta(0, 0)
        for i in first_gap_list:
            first_sum_time = first_sum_time + i
        for j in sec_gap_list:
            sec_sum_time = sec_sum_time + j
        first_avg_time = first_sum_time / len(first_gap_list)
        sec_avg_time = sec_sum_time / len(sec_gap_list)

        if int(interval_time[1][:4]) - int(interval_time[0][:4]) == 1:
            time_axis = interval_time[0][:4] + '下半年'
        elif int(interval_time[1][:4]) - int(interval_time[0][:4]) == 0:
            time_axis = interval_time[0][:4] + '上半年'
        else:
            time_axis = 'Wrong'
        print(self.history_name)
        print(Fore.GREEN + '平均回复' + '【' + self.first_strike_up + '】' + '的时间是：' + str(first_avg_time))
        print(Fore.GREEN + '平均回复' + '【' + self.sec_strike_up + '】' + '的时间是：' + str(sec_avg_time))
        return [time_axis, first_strike_up, sec_avg_time]

    def get_time_gap(self):
        if not self.chat_his:
            self.get_chat_his()
        self.year_time = len(self.chat_his[:-2])

        for year in self.chat_his[:-2]:
            self.time_gap.append(str(year) + '-01-01')
            self.time_gap.append(str(year) + '-06-30')
        # 若存在最初日期大于六月份
        log(self.chat_his)
        if not self.chat_his[-2]:
            self.time_gap = self.time_gap[1:]
        if not self.chat_his[-1]:
            self.time_gap = self.time_gap[:-1]
        log('your time_gap %s' % self.time_gap)
        return self.time_gap

    def get_reply_fluency(self, time_gap=None):
        appear_name_list = self.get_field(2, time_gap)
        fluency_table = Counter(appear_name_list)
        first_frequency = fluency_table[self.first_strike_up] / len(appear_name_list)
        sec_frequency = 1 - first_frequency
        first_ratio_reply = first_frequency / sec_frequency
        sec_ratio_reply = sec_frequency / first_frequency
        print(self.first_strike_up + "回复频率为 1: " + "%.2f" % first_ratio_reply)
        print(self.sec_strike_up + "回复频率为 1: " + "%.2f" % sec_ratio_reply)
        onedict=dict()
        secdict=dict()
        back_json={}
        first_name_fluency=self.first_strike_up + "回复频率"
        sec_name_fluency=self.sec_strike_up+'回复频率'
        onedict["name"]=first_name_fluency
        onedict["value"]=first_ratio_reply*100
        secdict["name"]=sec_name_fluency
        secdict["value"]=sec_ratio_reply*100
        back_json['x_data']=[first_name_fluency,sec_name_fluency]
        back_json['y_data']=[onedict, secdict]
        self.json2file(back_json,'reply_ratio.json')
        return back_json

    def get_content_ratio(self, time_gap=None):
        first_content_list = ''.join(self.get_field(1, time_gap, 'qq_user', self.first_strike_up))
        first_content_length = len(first_content_list)
        sec_content_list = ''.join(self.get_field(1, time_gap, 'qq_user', self.sec_strike_up))
        sec_content_length = len(sec_content_list)
        first_ratio_content = first_content_length / sec_content_length
        sec_ratio_content = sec_content_length / first_content_length
        print(self.first_strike_up + "内容回复比率为 1: " + "%.2f" % first_ratio_content)
        print(self.sec_strike_up + "内容回复比率为 1: " + "%.2f" % sec_ratio_content)
        # 这里重新初始化
        onedict=dict()
        secdict=dict()
        back_json={}
        first_name_content = self.first_strike_up + "内容回复比率"
        sec_name_content = self.sec_strike_up + '内容回复比率'
        onedict["name"] = first_name_content
        onedict["value"] = first_ratio_content * 100
        secdict["name"] = sec_name_content
        secdict["value"] = sec_ratio_content * 100
        back_json['x_data'] = [first_name_content, sec_name_content]
        back_json['y_data'] = [onedict, secdict]
        self.json2file(back_json, 'content_ratio.json')
        return back_json

    def jieba_count_word(self, time_gap=None):
        jieba.set_dictionary('foobar.txt')
        # 有些聊天词语 字典加了也不给划分 因此我在这里强制一下
        jieba.suggest_freq(('会从', '[表情]'))
        msg_list = self.get_field(1, time_gap)
        count_gap_word = {}
        for single_msg in msg_list:
            cut_sentence = jieba.cut(single_msg)
            for word in cut_sentence:
                if not count_gap_word.get(word, None):
                    count_gap_word.setdefault(word, 1)
                if not self.count_word.get(word, None):
                    self.count_word.setdefault(word, 1)
                else:
                    plus_one = count_gap_word[word] + 1
                    fuck_one = self.count_word[word] + 1
                    count_gap_word[word] = plus_one
                    self.count_word[word] = fuck_one

                    # print(count_gap_word)
        jieba_count = sorted(self.dict2list(count_gap_word), key=lambda x: x[1], reverse=True)
        # print(jieba_count)
        return jieba_count

    def make_tag_pic(self, tag_list):
        # 获取工作路径
        file_path = os.getcwd()

        # 生成词云图
        wl = ",".join(tag_list)
        foot_path = file_path + '\\show\\font\\造字工房尚黑G0v1常规体.otf'
        save_path = file_path + '\\show\\pic\\词云图.jpg'
        # print(save_path)
        # 设置背景图片路径
        abel_mask = np.array(Image.open(file_path + '\\show\\ciyun\\background_image\\love .jpg'))

        wc = WordCloud(background_color="black",  # 设置背景颜色
                       mask = abel_mask,  #设置背景图片
                       max_words=200,  # 设置最大显示的字数
                       # stopwords = "", #设置停用词
                       # 这里注意兼容 linux 版本 以及font 字体
                       font_path=foot_path,
                       # 设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文）
                       max_font_size=100,  # 设置字体最大值
                       random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
                       scale=1.5   #设置保存的词云图尺寸大小
                       )

        myword = wc.generate(wl)  # 生成词云
        # 这里将图片存放到pic 文件夹里面
        wc.to_file(save_path)
        # 展示词云图
        plt.title("LoveTime")
        plt.imshow(myword)
        plt.axis("off") # figure（显示窗口）默认是带axis（坐标尺）的，如果没有需要，我们可以关掉
        plt.show()

    def json2file(self,dict,filename):
        file_path=os.getcwd()+'\\show\\json\\'+filename
        f=open(file_path,'w',encoding='utf-8')
        f.write(str(dict).replace("'",'"').replace('True', 'true'))
        print(Fore.GREEN+'Set up %s success'%filename)

    def make_calenda_data(self, time_list=None):
        time_list=self.time_gap
        calendar_list=[]

        for count in range(len(time_list)-1):
            single_calendar = {}
            my_range=[time_list[count],time_list[count+1]]
            my_top=100+240*count
            # 这里防止2016 进行干扰月份判定 所以选择[4:]
            if str(6) in str(time_list[count])[4:]:
                my_formatter='{start}'+' 下半年'
            else:
                my_formatter = '{start}' + ' 上半年'
            single_calendar["left"]="center"
            single_calendar["range"]=my_range
            single_calendar["top"]=my_top
            single_calendar["splitLine"]={
            "show": True,
            "lineStyle": {
                "color": '#000',
                "width": 4,
                "type": 'solid'
            }}
            single_calendar["yearLabel"]={
            "formatter": my_formatter,
            "textStyle": {
                "color": '#fff'
            }
        }
            single_calendar["itemStyle"]={
            "normal": {
                "color": '#323c48',
                "borderWidth": 1,
                "borderColor": '#111'
            }
        }
            calendar_list.append(single_calendar)
        print(calendar_list)
        back_json={"data":calendar_list}
        self.json2file(back_json,'calendar.json')
        return calendar_list
# 这些复杂的函数 到时还是写一个unittest
if __name__ == "__main__":
    moniter = moniter_platform()
    count = 0
    moniter.get_time_gap()
    print(moniter.time_gap[:-1])
    for gap in moniter.time_gap[:-1]:
        print(moniter.time_gap[count + 1])
        small_gap = [moniter.time_gap[count], moniter.time_gap[count + 1]]
        moniter.reply_rate(small_gap)
        moniter.get_reply_fluency(small_gap)
        moniter.get_content_ratio(small_gap)
        moniter.jieba_count_word(small_gap)
        count += 1
    # print(sorted(moniter.dict2list(moniter.count_word), key=lambda x: x[1], reverse=True))
    # file_path = get2db().get_path()
    # content = ''.join(moniter.get_field(1))
    #
    # # todo 长度是需要变化的
    # tags = jieba.analyse.extract_tags(content, 40)
    # print(",".join(tags))
    # moniter.make_tag_pic(tags)
    # my_dict=moniter.visual_time()
    moniter.get_reply_fluency()
    moniter.get_content_ratio()
    moniter.make_calenda_data()

