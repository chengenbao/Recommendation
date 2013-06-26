#!/usr/bin/python
# FileName: Config.py


class Config:
    def __init__(self):
        self.__config = {}
        try:
            f = open("config.ini")
            for line in f:
                tmp = line.split()
                for ent in tmp:
                    index = ent.find("=")
                    if index == -1:
                        self.__config[ent] = True
                    else:
                        key = ent[:index]
                        value = ent[index + 1:]
                        self.__config[key] = value
            f.close()
        except IOError:
            print "parse file error"

    def get_config(self, key):
        value = None
        if key in self.__config:
            value = self.__config[key]
        return value
    def add_config(self, key, value) :
        self.__config[key] = value
    def set_config(self, key, value) :
        self.__config[key] = value

config = Config()

if __name__ == "__main__":
    print dir(Config)
