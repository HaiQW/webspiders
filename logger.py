import logging
import logging.config

logging.config.fileConfig("./log/logging.conf")

# create logger
logger_name = "zhihu"
logger = logging.getLogger(logger_name)

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
