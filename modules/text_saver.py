from datetime import datetime
import os

from modules.exceptions import FileSaverException

class ResultSaver:

    __file = None
    __path = ""

    def __init__(self):
        pass

    def open_file(self, path, device):
        if not path:
            path = "./results/" + device + datetime.now().strftime("_%Y-%m-%d_%H_%M") + "_test.csv"
        self.__path = path
        try:
            log = open(self.__path, "w")
            self.__file = log
        except:
            raise FileSaverException("Unable to open file to save results")

    def close_file(self):
        if self.__file:
            self.__file.close()

    def return_file_path(self):
        return self.__path

    def save_results(self, results, deviceInfo):
        for line in deviceInfo:
            self.__write_to_file(line + "\n")
        header = "Command; Arguments; Expects; Result; Status\n"
        self.__write_to_file(header)
        for result in results:
            formatedString = self.__format_string(result)
            self.__write_to_file(formatedString)

    def __write_to_file(self, string):
        self.__file.write(string)

    def delete_empty_file(self):
        if os.stat(self.__path).st_size == 0:
            os.remove(self.__path)

    def __format_string(self, result):
        return result["command"] + "; " + str(result["arguments"]) + "; " + str(result["expects"]) + "; " + str(result["response"]) + "; " + result["status"] + "\n"
