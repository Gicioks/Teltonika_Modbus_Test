# Teltonika MODBus register value test

Program that tests MODBus register values compared them to OpenWRT MicroBus, gsmdctl module values

Program tests any device from device list in config file when given parameter `-D`, for example: `sudo python3 ./main.py -D RUTX11`.

Note: the device must defined in config file. 
Config JSON file [example](config.json). 

It connects to device via SSH and MODBus TCP to test MODBus returned values.
The program reads all data of a given device from config file (or default argument values) if such device exists. 
A connection is established if given parameters are correct (Device IP address, MODBus port, SSH port, auth credentials, etc.) and if the device is connected and is avaliable.

Program tests if given register address value is as axpected (_see config file [example](config.json)_) and forms result file.

Example result file:

![image](https://user-images.githubusercontent.com/61172051/168070484-c8b7b992-4e5c-4058-9dde-883d23ada6ba.png)

Example program output:

![image](https://user-images.githubusercontent.com/61172051/168070573-825d15f7-1eb5-4f5f-86ef-8fd73ff64535.png)

## Setup
Install Python 3.9.x with pip:
```
sudo apt update
sudo apt install python3.9 python3-pip
```
Install listed packages:

- [pyModbusTCP](https://pypi.org/project/pyModbusTCP/)
- [Paramiko](https://docs.paramiko.org/)
- [reprint](https://github.com/Yinzo/reprint)
```
pip3 install pyModbusTCP
pip3 install paramiko
pip3 install reprint
```

## Usage
Run program as sudo with parameters: `sudo python3 ./main.py -D {device}`. For more information run `python3 ./main -h`

Note: when connecting to devices via serial port, make sure ModBus is enabled under services tab.
## Flags
Default flag values:
- General flags:
  - Device name: (`-D, --device`) no default value, **the device must be specified by the user**.
  - IP address (`-a" | --ip`) default value - `'192.168.1.1'
- SSH flags:
  - SSH port: (`-pS | --serial-port`) default value - `22`
  - SSH IP address: (`-a | --ip`) default value - `'192.168.1.1'`
  - SSH user username: (`-u | --user`) default value - `'root'`
  - SSH user password: (`-p | --password`) default value - `'Admin123'`
- MODBus flags:
  - MODBus port: (`-pM, --modbus-port`) default value - `502`
