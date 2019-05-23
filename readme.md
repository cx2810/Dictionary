1.确定技术
    通信  tcp通信
    并发  多进程并发
    数据库 mysql

2.确定数据库：建立几个表，每个表作用和存储内容

    建表
        单词表words：id,word，mean
        用户表user：id,name,passwd
        记录表hist：id,name,word,time

    编写程序将单词本存入到数据库

3.结构设计
    客户端

    服务端


4.功能分析

    客户端和服务端分别需要实现哪些功能
    网络模型
    注册
        客户端 * 输入注册信息
              * 发送注册信息
              * 等待反馈消息

协议制定：注册 R name passwd
        登录 L name passwd
        查找 F name word
        记录 K name
        退出 Q



    客户端
        一级界面
            注册:输入用户名
                发送用户名
                接收返回结果，不存在则输入密码，存在则返回输入用户名
                接收返回结果，
                    注册成功，进入二级界面
                    注册失败，重新注册
            登录:输入用户名和密码
                发送用户名和密码
                接收返回结果,
                    登录成功,进入二级界面
                    登录失败,重新登录
            退出:发送退出消息
                接收返回结果
                服务端退出
        二级界面
            查单词:
                输入单词
                发送单词
                返回结果
            历史记录
                输入历史记录
                发送消息
                返回结果
            注销:发送注销消息
                接收返回结果
                服务端退出
                返回一级界面


    服务端(处理数据，函数)
        一级界面
            注册：接收用户名
                检查用户名是否存在，返回消息
                接收密码
                返回结果，user表添加用户名和密码
            登录：接收用户名和密码
                检查用户名和密码是否正确,返回消息
            注销：
                接收消息
                返回结果
        二级界面
            查单词：接收单词
                查找单词解释
                返回结果
            历史记录：接收查询历史记录消息
                查找历史记录
                返回结果
            注销：
                接收消息
                断开连接