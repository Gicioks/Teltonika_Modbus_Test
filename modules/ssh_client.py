from time import sleep
import paramiko
from modules.exceptions import SSHConnectionException, SSHRetryException
from modules.console_printer import ConsolePrinter

class SshHandler:

    __ssh_client = None
    __shell = None
    __device = None
    __error_printer = None

    def __init__(self, config, args):
        addr = args.get_addr()
        username = args.get_ssh_user()
        password = args.get_ssh_password()
        port = args.get_ssh_port()
        self.__device = config.get_param("device")
        self.__error_printer = ConsolePrinter(1)
        if not self.__open_connection(addr, username, password, port):
            raise SSHConnectionException("Unable to connect to SSH server")

        sleep(0.1)
        self.__clear_shell()
        # self.__print()

    ###
    # Connection operations

    def __open_connection(self, addr, username, password, port):
        success = False
        counter = 0
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        while counter <= 5 and not success:
            counter += 1
            try:
                client.connect(addr, port, username, password, auth_timeout=10, timeout=10)
                self.__ssh_client = client
                self.__shell = self.__ssh_client.invoke_shell()

                success = True
            except:
                if counter <= 5:
                    self.__error_printer.update_line(0, self.__error_printer.string_style("33", "Unable to connect to SSH server, retrying... " + str(counter)))
                    sleep(1)
        
        return success

    def __close_connection(self):
        if self.__ssh_client:
            self.__ssh_client.close()

    ###
    # read/write operations

    def __read_shell(self, expects=None):
        buffer = None

        success = False
        counter = 0
        while counter <= 5 and not success:
            counter += 1

            try:
                msWait = 0
                while (msWait <= 500 and not self.__shell.recv_ready):
                    msWait += 1
                    sleep(0.001)
                temp = self.__shell.recv(nbytes=2147483647)

                if temp:
                    buffer = temp.decode()
                    success = True
            except:
                if counter <= 5:
                    self.__error_printer.update_line(0, self.__error_printer.string_style("33", "Could not read shell, retrying... " + str(counter)))
                    sleep(1)
                else:
                    return None

        return buffer

    def __write_shell(self, data):
        # self.__clear_buffer()

        success = False
        counter = 0
        while counter <= 5 and not success:
            counter += 1

            try:
                self.__shell.send(data + "\r")
                success = True
            except:
                if counter <= 5:
                    self.__error_printer.update_line(0, self.__error_printer.string_style("33", "Could not write to shell, retrying... " + str(counter)))
                    sleep(1)

        return success

    ###
    # Command operations

    def exec_command_shellinvoke(self, command, arguments=None):
        success = True
        response = None

        self.__clear_shell()

        if not self.__write_shell(command):
            raise SSHConnectionException("Connection to SSH server lost")

        if arguments:
            for arg in arguments:
                sleep(0.5)
                if not self.__write_serial(arg):
                    raise SSHConnectionException("Connection to SSH server lost")

        response = self.__read_shell()

        if response is None:
            raise SSHConnectionException("Connection to SSH server lost")

        # if not self.__check_response(response, expects):
        #     success = False

        return response#, success

    def exec_command(self, command):
        success = True
        response = None

        try:
            stdin, stdout, stderr = self.__ssh_client.exec_command(command, get_pty=True)            
            stdoutOutput = stdout.read()
            stderrOutput = stderr.read()
            
            response = stdoutOutput.decode()
            
            if not stderrOutput or len(stderrOutput) == 0:
                success = False
        except:
            raise SSHConnectionException("Connection to SSH server lost")
            
        return response#, success

    ###
    # Misc operations
    
    def __clear_shell(self):
        self.__write_shell("clear")

    def __del__(self):
        if self.__ssh_client:
            self.__close_connection()
        # self.__error_printer.close()