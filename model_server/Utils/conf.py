#coding:utf-8
import configparser as cg


class Config():
    def __init__(self,conf_path):
        self.conf = cg.ConfigParser()
        self.data = conf_path
        self.conf.read(self.data,encoding='utf-8')

    def getQiNiuAccessKey(self):
        try:
            key = self.conf.get('QINIUYUN','access_key')
            key = str(key)
        except Exception as e:
            print e
            return None
        return key

    def getQiNiuSecretKey(self):
        try:
            key = self.conf.get('QINIUYUN','secret_key')
            key = str(key)
        except Exception as e:
            print e
            return None
        return key

    def getDataBaseInfo(self):
        section = 'MYSQL'
        if self.conf.has_section(section):
            dataBaseInfo = self.conf.items(section)
            result = [str(info[1]) for info in dataBaseInfo]
        else:
            result = []
        return result

    def getHost(self):
        try:
            key = self.conf.get('SERVER','host')
            key = str(key)
        except Exception as e:
            print e
            return None
        return key

    def getPort(self):
        try:
            key = self.conf.get('SERVER','port')
            key = str(key)
        except Exception as e:
            print e
            return None
        return key

if __name__ == '__main__':
    conf = Config('config.conf')
    dataBaseInfo = conf.getDataBaseInfo()
    print dataBaseInfo
