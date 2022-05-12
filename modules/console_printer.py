from reprint import output
from modules.exceptions import ModuleInitializeException, ConsolePrinterException

class ConsolePrinter:

    __console_ourput = None
    __console_print_list = None

    __total = 0
    __current = 0
    __passed = 0
    __failed = 0

    def __init__(self, length=0, total=0) -> None:

        self.__console_ourput, self.__console_print_list = self.__create_output_object(length)
        self.__total = total
        if total:
            self.__create_test_output()
       
        if not self.__console_ourput and not self.__console_print_list:
            raise  ModuleInitializeException("Unable to create console printer object")

    def __create_output_object(self, length):
        # default formatting for test cases
        if length == 0:
            console_output = output(output_type="list", initial_len=4, interval=0)
        # if needed custom for other purposes
        else:
            console_output = output(output_type="list", initial_len=length, interval=0)
        
        print_list = console_output.warped_obj
        
        return console_output, print_list

    # Single line operations
    def update_line (self, index, line):
        self.__console_print_list[index] = line

    def get_line (self, index):
        return self.__console_print_list[index]
    
    # String style
    def string_style(self, style, string):
        return ("\033[" + style + "m" + string + "\033[00m")

    # Test output updater
    ### 
    # Format:
    # Test case {current} out of {total}:
    # Command: {command} {args}
    # Command {command} status: "Pass" | "Fail"
    # Passed: {passed} Failed: {failed}

    def __create_test_output(self):
        self.__update_top()
        self.__update_case()
        self.__update_status()
        self.__update_bottom()
    
    def close(self):
        self.__console_ourput.__exit__(None, None, None)
    
    def update_test_output(self, command):
        self.__current += 1
        self.__update_top()
        self.__update_case(command)
    def update_result_output(self, status=None, command="N/A"):
        if status is not None and status is True:
            self.__passed += 1
        elif status is not None and status is False:
            self.__failed += 1

        self.__update_status(status, command)
        self.__update_bottom()

    def clear_result_output(self):
        self.__update_status()
        self.__update_bottom()

    def __update_top(self):
        line = "Test case: " + str(self.__current) + " out of " + str(self.__total)
        self.__console_print_list[0] = line
    def __update_case(self, regAddr = "N/A"):
        line = "Register address: " + str(regAddr)
        self.__console_print_list[1] = line
    def __update_status(self, status=None, regAddr="N/A"):
        line = "Register addres :" + str(regAddr) + " status: "
        if status is not None and status is True:
            line += self.string_style("32", "Passed")
        elif status is not None and status is False:
            line += self.string_style("31", "Failed")
        self.__console_print_list[2] = line
    def __update_bottom(self):
        line = "Passed: " + self.string_style("32", str(self.__passed)) +"; " + "Failed: " + self.string_style("31", str(self.__failed))
        self.__console_print_list[3] = line