#coding:utf-8
import logging

class MyLog():
    def __init__(self,filename,level=logging.DEBUG):


        self.logger = logging.getLogger(filename)
        self.logger.setLevel(level)
        record ='%(asctime)s [%(levelname)s] %(message)s'
        formatter = logging.Formatter(record,'%Y-%m-%d %H:%M:%S')
        fh = logging.FileHandler(filename,'a')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        # logging.basicConfig(level=level,
        #             format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        #             datefmt='%a, %d %b %Y %H:%M:%S',
        #             filename=filename,
        #             filemode=filemode)
    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)

    def warning(self,message):
        self.logger.warning(message)

    def error(self,message):
        self.logger.error(message)

    def critical(self,message):
        self.logger.critical(message)


if __name__ == '__main__':

    log = MyLog('1234.log')
    #log = MyLog('123.log')
    log.debug('debug message吞吞吐吐')
    log.info('info message')
    log.warning('warning message')
    log.error('error message')
    log.critical('critical message')
    log.info('dadadada%s%s'%(1,'11'))