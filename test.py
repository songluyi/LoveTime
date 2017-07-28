# -*- coding: utf-8 -*-
# 2017/6/24 14:42
"""
-------------------------------------------------------------------------------
Function:
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
#
# import pymysql
# db = pymysql.connect(host='localhost',
#                             port=3308,
#                              user='sly',
#                              password='070801382',
#                              db='work',charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor )
#
#
# cursor = db.cursor()
#
# sql='select DISTINCT 批号 from 电池片汇总2'
# # 使用 execute()  方法执行 SQL 查询
# cursor.execute(sql)
# bottole = []
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchall()
# for i  in data:
#     plus_sql='select * from 电池片汇总2 where 批号='+'"'+i['批号']+'"'
#     # print(plus_sql)
#     cursor.execute(plus_sql)
#     new_data=cursor.fetchall()
#     count=0
#
#     if len(new_data)>1:
#         # print(i)
#         for j in new_data[1:]:
#             if new_data[0]['效率']!=j["效率"] or new_data[0]['颜色']!=j["颜色"] or new_data[0]['细等级']!=j["细等级"]:
#                 if i not in bottole:
#                     bottole.append(i)
#                     # print(bottole)
# print(bottole)
#         # # print(new_data)
#         # for j in new_data[1:]:
#         #     count+=1
#         #     new_batch=str(i["批号"])+'-S'+str(count)
#         #     print(j)
#         #     update_sql='update 电池片汇总 set 批号 ='+'"'+ new_batch+'"'+'where 导入序号='+str(j["导入序号"])
#         #     print(update_sql)
#         #     cursor.execute(update_sql)
#
# # print ("Database version : %s " % data)
# # db.commit()
# # 关闭数据库连接
#
# db.close()
print(int('04'))

