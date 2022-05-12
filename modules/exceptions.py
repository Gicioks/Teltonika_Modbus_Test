###
# Module init exception

from email import message


class ModuleInitializeException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)

###
# Argument handler exceptions

class ArgumentHandlerException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

###
# Config handler exceptions

class ConfigHandlerException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

###
# Console printer exceptions

class ConsolePrinterException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

###
# Result handler exception

class ResultHandlerException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

###
# Modbus client exceptions

class ModbusConnectionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class ModbusRetryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

###
# SSH cleint exceptions

class SSHConnectionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class SSHRetryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

###
# Test handler exceptions

class TestHandlerException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

###
# File saver exceptions

class FileSaverException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CSVSaverException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class TextSaverException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)