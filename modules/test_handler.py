from modules.console_printer import ConsolePrinter
from modules.value_parser import ValueParser

class TestHandler:

    __ssh = None
    __modbus = None
    __value_parser = None
    __results = []
    __device_info = []
    __printer = None

    def __init__(self, ssh, modbus):
        self.__ssh = ssh
        self.__modbus = modbus
        self.__value_parser = ValueParser(ssh)
        # self.__device_info = connection.get_device_info()
        # if not self.__device_info:
            # raise ModuleInitializeException ("Unable to get device info")

    def test_modbus_values(self, registers):
        self.__printer = ConsolePrinter(total=len(registers))
        for index, register in enumerate(registers):
            result = {}
            value, check_value, status = self.test_modbus_value(register["register"], register["type"], register["check_function"])
            result["register"] = register["register"]
            result["type"] = register["type"]
            result["check_value"] = check_value
            result["value"] = value
            result["status"] = status
            self.__results.append(result)
    
    def test_modbus_value(self, register, type, check_function):
        response = None
        success = False

        self.__printer.update_test_output(register)
        self.__printer.clear_result_output()

        # If incorrect register types (not uint32, int32, uint16, int16, float, text)
        if not (type.lower() == "uint32" or type.lower() == "int32" or
                type.lower() == "uint16" or type.lower() == "int16" or
                type.lower() == "float" or type.lower() == "text"):
            self.__printer.update_result_output(False, register)
            response = "Incorrect regsiter type"

            return response, response, "Failed"

        if type.lower() == "uint32":
            value = self.__modbus.get_uint(register, 2)
        elif type.lower() == "int32":
            value = self.__modbus.get_int(register, 2)
        elif type.lower() == "uint16":
            value = self.__modbus.get_uint(register, 1)
        elif type.lower() == "int16":
            value = self.__modbus.get_int(register, 1)
        elif type.lower() == "float":
            value = self.__modbus.get_float(register, 2)
        elif type.lower() == "text":
            value = self.__modbus.get_string(register, 16)
        
        check_value, success = getattr(self.__value_parser, check_function.lower())(value)
        if success:
            self.__printer.update_result_output(True, register)
            return str(value), str(check_value), "Passed"
        else:
            self.__printer.update_result_output(False, register)
            return str(value), str(check_value), "Failed"
    
    def get_results(self):
        return self.__results
    def get_device_info(self):
        return self.__device_info

    def close_printer(self):
        self.__printer.close()