import argparse
from curses import meta
from modules.exceptions import ModuleInitializeException, ArgumentHandlerException

class ArgHandler:

    __argHandler = None

    def __init__(self) -> None:
        
        if not self.__parse_args():
            raise ModuleInitializeException("Unable to parse arguments")
    
    def __parse_args(self):
        parser = argparse.ArgumentParser()
        # general args
        parser.add_argument("-D", "--device", dest="device", help="Device name", required=True)
        # ssh args
        parser.add_argument("-pS", "--serial-port", dest="ssh_port", default=22, help="SSH port", required=False)
        parser.add_argument("-a", "--ip", dest="ip", default="192.168.1.1", help= "SSH/ModBus IP", required=False)
        parser.add_argument("-u", "--user", dest="ssh_username", default="root", help="SSH user username", required=False)
        parser.add_argument("-p", "--password", dest="ssh_password", default="Admin123", help="SSH user password", required=False)
        # modbus args
        parser.add_argument("-pM", "--modbus-port", dest="modbus_port", default=502, help="ModBus port", required=False)
    
        try:
            self.__argHandler = parser.parse_args()
        except Exception:
            return False

        return True

    def get_args(self):
        if self.__argHandler:
           return self.__argHandler
        else:
            return None

    def print_args(self):
        if self.__argHandler:
            print(self.__argHandler)
    
    ###
    # general args

    def get_device(self):
        if self.__argHandler:
           return self.__argHandler.device.strip()
        else:
            return None
    def get_addr(self):
        if self.__argHandler:
            return self.__argHandler.ip.strip()
        else:
            return None

    ###
    # SSH args

    def get_ssh_port(self):
        if self.__argHandler:
            return self.__argHandler.ssh_port
        else:
            return None
    def get_ssh_user(self):
        if self.__argHandler:
            return self.__argHandler.ssh_username.strip()
        else:
            return None
    def get_ssh_password(self):
        if self.__argHandler:
            return self.__argHandler.ssh_password.strip()
        else:
            return None
    
    ###
    # Modbus args

    def get_modbus_port(self):
        if self.__argHandler:
            return self.__argHandler.modbus_port