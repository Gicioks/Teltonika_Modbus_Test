from cgi import test
import modules.arg_handler as ArgHandler
import modules.config_handler as ConfigHandler
import modules.modbus_client as ModbusHandler
import modules.ssh_client as SshHandler
import modules.test_handler as TestHandler
import modules.result_handler as ResultHandler
from modules.console_printer import ConsolePrinter
from modules.exceptions import *

args: ArgHandler.ArgHandler = None
config: ConfigHandler.ConfigHandler = None
ssh: SshHandler.SshHandler = None
modbus: ModbusHandler.ModbusHandler = None
tester: TestHandler.TestHandler = None
resulter: ResultHandler.ResultHandler = None
error_printer: ConsolePrinter = None

def init_modules():
    global args, config, ssh, modbus, tester, resulter, error_printer
    try:
        error_printer = ConsolePrinter(length=1)
        args = ArgHandler.ArgHandler()
        config = ConfigHandler.ConfigHandler("config.json")
        config.load_config_device(config.get_indexOf_device(args.get_device()))
        ssh = SshHandler.SshHandler(config, args)
        modbus = ModbusHandler.ModbusHandler(config, args)
        tester = TestHandler.TestHandler(ssh, modbus)
        resulter = ResultHandler.ResultHandler(config.get_param("results")["format"])
    except Exception as error:
        raise error


def main():
    try:
        init_modules()
        # args.print_args()
        resulter.open_file(args.get_device().upper())
        tester.test_modbus_values(config.get_param("registers"))
        resulter.save_results(tester.get_results(), tester.get_device_info())
        tester.close_printer()
        resulter.close_file()
        error_printer.close()

    # Exception handling:
    except (ModuleInitializeException, ConfigHandlerException, FileSaverException, ModbusConnectionException, SSHConnectionException) as error:
        error_printer.update_line(0, error_printer.string_style("31", str(error)))
        error_printer.close()
        if resulter:
            resulter.delete_empty_file()
        return
    except KeyboardInterrupt:
        error_printer.update_line(0, error_printer.string_style("31", "Keyboard interrupt detected, exiting..."))
        error_printer.close()
        if resulter:
            resulter.delete_empty_file()
        return

    except Exception as error:
        error_printer.update_line(0, error_printer.string_style("1;31", "Unhandled exception: ") + error_printer.string_style("31", str(error)))
        error_printer.close()
        if resulter:
            resulter.delete_empty_file()
        return

if __name__ == "__main__":
    main()