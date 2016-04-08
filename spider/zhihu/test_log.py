#-*- coding: utf-8 -*-
import logging

# 创建logger
logger_name = "example"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

# 创建过滤
log_path = './log.log'
fh = logging.FileHandler(log_path)
fh.setLevel(logging.WARN)

# 创建格式
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datafmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datafmt)

# 添加hander
fh.setFormatter(formatter)
logger.addHandler(fh)

# 记录
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')

