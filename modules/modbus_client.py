import struct
from time import sleep
import win_inet_pton
# from pymodbus.client.sync import ModbusTcpClient #broken register read ant connection... (conn auto closes)
from pyModbusTCP.client import ModbusClient
from modules.console_printer import ConsolePrinter
from modules.exceptions import ModbusConnectionException
import re

class ModbusHandler:

    __modbus_client = None
    __device = None
    __error_printer = None

    def __init__(self, config, args):
        addr = args.get_addr()
        port = args.get_modbus_port()
        self.__device = config.get_param("device")
        self.__error_printer = ConsolePrinter(1)
        if not self.__open_connection(addr, port):
            raise ModbusConnectionException("Unable to connect to ModBus server")

        # self.__print()

    ###
    # Connection operations

    def __open_connection(self, addr, port):
        success = False
        counter = 0
        while counter <= 5 and not success:
            counter += 1
            try:
                # self.__modbus_client = ModbusTcpClient(host=addr, port=port)
                # self.__modbus_client.connect()
                self.__modbus_client = ModbusClient(host=addr, port=port, auto_open=True, auto_close=False)

                success = True
            except:
                if counter <= 5:
                    self.__error_printer.update_line(0, self.__error_printer.string_style("33", "Unable to connect to ModBus server, retrying... " + str(counter)))
                    sleep(1)
        
        return success

    def __close_connection(self):
        if self.__modbus_client:
            self.__modbus_client.close()

    ###
    # read/write operations

    def __read_registers(self, fromReg, count):
        registers = []

        success = False
        counter = 0
        while counter <= 5 and not success:
            counter += 1

            try:
                msWait = 0
                while msWait <= 50 and not success: # if response is long wait 5 sec
                    msWait += 1
                    temp = self.__modbus_client.read_holding_registers(fromReg, count)
                    if temp:
                        registers = temp
                        success = True
                    else:
                        sleep(0.1)
            except:
                if counter <= 5:
                    self.__error_printer.update_line(0, self.__error_printer.string_style("33", "Could not read ModBus registers, retrying... " + str(counter)))
                    sleep(1)
                else:
                    return None

        return registers
    
    def __write_registers(self, fromReg, regValues):
        success = False
        counter = 0
        while counter <= 5 and not success:
            counter += 1

            try:
                success = self.__modbus_client.write_registers(fromReg, regValues)
            except:
                if counter <= 5:
                    self.__error_printer.update_line(0, self.__error_printer.string_style("33", "Could not write to ModBus registers, retrying... " + str(counter)))
                    sleep(1)

        return success
    def __write_single_register (self, register, value):
        success = False
        counter = 0
        while counter <= 5 and not success:
            counter += 1

            try:
                success = self.__modbus_client.write_register(register, value)
            except:
                if counter <= 5:
                    self.__error_printer.update_line(0, self.__error_printer.string_style("33", "Could not write to ModBus register, retrying... " + str(counter)))
                    sleep(1)

    ###
    # Register parse operations
        # Unsigned int
    def get_uint(self, regAddr, length):
        regList = self.__read_registers(regAddr, length)

        if regList is None:
            return None
        elif len(regList) == 0:
            return None
        
        byteArr = self.__registers_to_bytes(regList)
        value = self.__bytes_to_uint(byteArr)

        return value
        # Signed int
    def get_int(self, regAddr, length):
        regList = self.__read_registers(regAddr, length)

        byteArr = self.__registers_to_bytes(regList)
        value = self.__bytes_to_int(byteArr)

        return value
        # Float
    def get_float(self, regAddr, length):
        regList = self.__read_registers(regAddr, length)

        if regList is None:
            return None
        elif len(regList) == 0:
            return None

        byteArr = self.__registers_to_bytes(regList)
        value = self.__bytes_to_float(byteArr)

        return value
        # String
    def get_string(self, regAddr, length):
        regList = self.__read_registers(regAddr, length)

        if regList is None:
            return None
        elif len(regList) == 0:
            return None

        byteArr = self.__registers_to_bytes(regList)
        value = self.__bytes_to_string(byteArr)

        return value

    ### 
    # Byte operations (conversions)

        # Registers to byteArray
    def __registers_to_bytes(self, regList):
        byteList = []
        for reg in regList:
            bytePair = int.to_bytes(reg, 2, byteorder='big')
            byteList.append(bytePair)
        byteArr = b''.join(byteList)

        return byteArr

    # From bytes to X
        #Signed int
    def __bytes_to_int(self, byteArr):
        return int.from_bytes(byteArr, byteorder="big", signed=True)
        # Unsigned int
    def __bytes_to_uint(self, byteArr):
        return int.from_bytes(byteArr, byteorder="big", signed=False)
        # Float (IEEE-754 convert)
    def __bytes_to_float(self, byteArr:bytes):
        reversedBytes:bytes = byteArr[::-1]
        value:float = struct.unpack('!f', reversedBytes)[0]
        return value
        #String
    def __bytes_to_string(self, byteArr): #ascii
        string = byteArr.decode().strip(b'\x00'.decode()) # dumb decode; decoder can't decode 0x00 byte correctly
        value = re.sub(" +", " ", string)
        return value
    
    
    # From X to bytes
    def __string_to_bytes(self, string): #ascii
        return bytearray(string.encode())
    def __int_to_bytes(self, int32:int):
        return int32.to_bytes()

    ###
    # Misc operations

    def __del__(self):
        if self.__modbus_client:
            self.__close_connection()
        # self.__error_printer.close()