# -*- coding:utf-8 -*-
"""
@Time 2021/2/3
@auth 码尚学院_百里老师
@Email 198977131@qq.com
@Content logger_util.py
"""
import logging
import os
import time

from util.common import get_object_path


class LoggerUtil:

    def create_log(self):
        #创建一个logger对象
        self.logger = logging.getLogger('log')
        #设置全局的日志级别
        self.logger.setLevel(logging.DEBUG)
        #判断这个日志对象中是否已经存在日志控制器
        if not self.logger.handlers:
            # print("-----------------文件日志--------------------")
            # 设置file日志文件的路径
            if not os.path.exists(get_object_path() + "logs/"):
                os.mkdir(get_object_path() + "logs/")

            self.log_file_path = get_object_path() + "logs/" + "log" + str(
                int(time.time())) + '.log'
            # 创建file日志的控制器
            self.file_handler = logging.FileHandler(self.log_file_path, encoding='utf-8')
            # 单独的设置文件日志的级别
            file_log_level = "debug"
            if file_log_level == 'debug':
                self.file_handler.setLevel(logging.DEBUG)
            elif file_log_level == 'info':
                self.file_handler.setLevel(logging.INFO)
            elif file_log_level == 'warning':
                self.file_handler.setLevel(logging.WARNING)
            elif file_log_level == 'error':
                self.file_handler.setLevel(logging.ERROR)
            elif file_log_level == 'critical':
                self.file_handler.setLevel(logging.CRITICAL)
            else:
                pass
            # 设置file日志的格式
            fmt='[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s] %(message)s'
            formatter = logging.Formatter(fmt=fmt)
            self.file_handler.setFormatter(formatter)
            # 将file日志的控制器加入日志对象
            self.logger.addHandler(self.file_handler)
            # print("-----------------控制台日志--------------------")
            # 创建console日志的控制器
            self.console_handler = logging.StreamHandler()
            # 单独的设置console日志的级别
            console_log_level = "debug"
            if console_log_level == 'debug':
                self.console_handler.setLevel(logging.DEBUG)
            elif console_log_level == 'info':
                self.console_handler.setLevel(logging.INFO)
            elif console_log_level == 'warning':
                self.console_handler.setLevel(logging.WARNING)
            elif console_log_level == 'error':
                self.console_handler.setLevel(logging.ERROR)
            elif console_log_level == 'critical':
                self.console_handler.setLevel(logging.CRITICAL)
            else:
                pass
            # 设置console日志的格式
            self.console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s] %(message)s'))
            # 将console日志的控制器加入日志对象
            self.logger.addHandler(self.console_handler)
            #关闭
            self.file_handler.close()
            self.console_handler.close()
        #返回
        return self.logger

#正确的日志
def log_info(log_message):
    LoggerUtil().create_log().info(log_message)


#错误的日志
def log_error(log_message):
    LoggerUtil().create_log().info(log_message)
    raise Exception(log_message)

# if __name__ == '__main__':
#     log_info("aaaa")