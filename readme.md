# LoveTime
#### **恋爱的好时光**
[![Travis](https://img.shields.io/travis/rust-lang/rust.svg)](https://github.com/songluyi/LoveTime)
[![PyPI](https://img.shields.io/pypi/wheel/Django.svg)](https://github.com/songluyi/LoveTime)
[![Hex.pm](https://img.shields.io/hexpm/l/plug.svg)](https://github.com/songluyi/LoveTime)

# For English speakers
This small tool is using for analyzing message of QQ as you want to know your 
friend and  u chat fluency ,chat rely ratio, favorite chat time,chat reply rate
and daily number of chats. 



# 效果展示
**1. 每半年（或每月）聊天回复速率**

      即：你发出消息后多少分钟后得到回复

**2. 一天中和TA 最爱聊天的时段**

**3. 在一段时间内聊天次数比率**

      即：你发出消息总次数/TA 发出消息总和次数

**4. 在一段时间内聊天内容长度比率**

      即：你发出消息总和长度/TA 发出消息总和长度

**5. 统计总时段内每天聊天总次数**

**6. 统计总时段内聊天标签和词频**

如图：
![](http://www.songluyi.com/wp-content/uploads/2017/08/恋爱的好时光.png)


# 升级版
1. 提供 【情感变化曲线】 录入的功能 和 【特别事件】 录入的功能.（特别事件指：约会吃饭交往俯卧撑等）

2. 对【特别事件】 情感因子 进行先期定义.

3. 提供 【情感变化曲线】 与 主要因变量【特别事件】 【聊天回复速率】【聊天次数比率】
【聊天内容长度比率】【每天聊天总次数】和【聊天标签和词频】时间面板数据之间的线性回归关系，进行建模。
最终将会提供线上交流和线下交流对情感Y影响比率，同时提供多重共线性判别结果.


# 使用方法
1. 首先从github上下载项目

   `git clone https://github.com/songluyi/LoveTime.git`
    
2. 然后进入项目目录

    `cd LoveTime`

3. 再安装依赖库

    `pip install -r requirements.txt`

4. 将QQ 聊天记录导出并放置到msg 文件夹下面

    **如何导出？**

    导出QQ消息记录：http://jingyan.baidu.com/article/a501d80c33919fec630f5e82.html

    **只能放置一个么**

    是的

5. 运行moniter.py

   ` python moniter.py`

## TO DO
1.	新增单元测试
2.  再写一个file接口方便单元测试或者是日后打包
2.  前端界面还可以再选择性优化一下 给人一种整体的感觉




