# -*- coding: utf-8 -*-
import ConfigParser
import os

# this is file config.ini charset.
__DEFAULT_CHARSET__ = 'utf-8'


class Config:
    def __init__(self, path, section=None):
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        self.section = section
        self.cf.read(path)

    def get(self, key, default_value=None, section=None):
        if section is None:
            section = self.section
        if default_value is not None:
            try:
                return self.get_unicode(section, key)
            except Exception, e:
                if isinstance(e, UnicodeDecodeError):
                    raise e
                else:
                    return default_value
        else:
            return self.get_unicode(section, key)

    def get_unicode(self, section, key):
        val = self.cf.get(section, key)
        if isinstance(val, str):
            val = val.decode(__DEFAULT_CHARSET__)
        return val

    def getint(self, key, default_value=None, section=None):
        if section is None:
            section = self.section
        if default_value is not None:
            try:
                return self.cf.getint(section, key)
            except:
                return default_value
        else:
            return self.cf.get(section, key)

    def getboolean(self, key, default_value=None, section=None):
        if section is None:
            section = self.section
        if default_value is not None:
            try:
                return self.cf.getint(section, key)
            except:
                return default_value
        else:
            return self.cf.getboolean(section, key)

    def getfloat(self, key, default_value=None, section=None):
        if section is None:
            section = self.section
        if default_value is not None:
            try:
                return self.cf.getint(section, key)
            except:
                return default_value
        else:
            return self.cf.getfloat(section, key)


def read_config(config_file_path, section, key):
    cf = ConfigParser.ConfigParser()
    cf.read(config_file_path)
    result = cf.get(section, key)
    return result


def write_config(config_file_path, section, key, value):
    cf = ConfigParser.ConfigParser()
    cf.read(config_file_path)
    cf.set(section, key, value)
    cf.write(open(config_file_path, 'w'))
    return True


if __name__ == '__main__':
    config = Config(os.path.pardir + "/config.ini", "pixiv")
    print config.getint("IMAGE_SVAE_BASEPATH")
