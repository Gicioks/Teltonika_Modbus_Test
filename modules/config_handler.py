import os
import json
from modules.exceptions import ModuleInitializeException, ConfigHandlerException

class ConfigHandler:

    __config = None
    __error = None

    def __init__(self, configPath="config.json"):
        if not self.__load_config(configPath):
            raise ModuleInitializeException(self.__error)

    def __load_config(self, configPath):
        if not os.path.exists(configPath):
            self.__error = "Config file does not exists"
            return None
        config = open(configPath, "r")
        content = config.read()
        if not self.__is_json(content):
            self.__error = "Config file content is not JSON"
            return None
        self.__config = json.loads(content)
        config.close()
        
        return True

    def load_config_device(self, index):
        if not self.__config:
            raise ConfigHandlerException("Config file is not loaded")
        try:
            arrayElem = self.get_param('devices')[index]
            if not arrayElem:
                raise ConfigHandlerException("Could not get device with index " + index)
            self.__config = arrayElem
        except Exception as error:
            raise ConfigHandlerException (error)

    def __is_json(self, content):
        try:
            json.loads(content)
        except:
            return False
        return True

    def get_indexOf_device(self, name):
        index = -1

        i = 0
        for device in self.__config['devices']:
            if device['device'].lower() == name.lower():
                index = i
                break
            i =+ 1

        if index < 0:
            raise ConfigHandlerException ("Device '" + name + "' config does not exist")
        return index

    def get_param(self, param):
        if param in self.__config.keys():
            return self.__config[param]
        else:
            return None