from xmlrpc.client import boolean

from modules.exceptions import ModuleInitializeException


class ResultHandler:

    __resultSaver = None

    def __init__(self, type):
        self.__resultSaver = self.__load_module(type)
        if not self.__resultSaver:
            raise ModuleInitializeException("Unable to load result handler module")
        self.__print_type(type)

    def __load_module(self, type):
        type = type
        module = None
        try:
            module = __import__('modules.{type}_saver'.format(type=type), fromlist=['modules'])
            return module.ResultSaver()
        except:
            return False

    def open_file(self, device, path=None):
        self.__resultSaver.open_file(path, device)
        self.__print_path()

    def close_file(self):
        self.__resultSaver.close_file()

    def save_results(self, results, deviceInfo):
        self.__resultSaver.save_results(results, deviceInfo)
    
    def delete_empty_file(self):
        self.__resultSaver.delete_empty_file()
    
    def __print_type(self, type):
        print("Result file type: " + type)
    def __print_path(self):
        print("Result file path: '" + self.__resultSaver.return_file_path() + "'\r\n")
