import json
import socket
from modules.ssh_client import SshHandler

class ValueParser:
    
    ssh_connection:SshHandler = None

    def __init__(self, ssh) -> None:
        self.ssh_connection = ssh

    # System uptime 32 bit unsigned integer
    def get_uptime(self, modbusVal):
        response = self.ssh_connection.exec_command("cat /proc/uptime")
        value = int(float(response.split()[0]))
        return value, abs(value - modbusVal) <= 5 or abs(value - modbusVal) >= 5 # 5 sec difference is ok
    # Mobile signal strength (RSSI in dBm)	32 bit integer
    def get_mobile_stength(self, modbusVal):
        response = self.ssh_connection.exec_command("gsmctl -q") 
        value = int(response)
        return value, modbusVal == value
    # System temperature (in 0.1 °C)	32 bit integer
    def get_temperature(self, modbusVal):
        response = self.ssh_connection.exec_command("gsmctl -c")
        value = int(response)
        return value, modbusVal == value
    # System hostname	Text
    def get_hostname(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call system board")
        jsonData = json.loads(response)
        value = jsonData['hostname']
        return value, modbusVal == value
    # GSM operator name	Text
    def get_gsm_operator(self, modbusVal):
        response = self.ssh_connection.exec_command("gsmctl -o")
        value = response
        return value, modbusVal == value
    # Router serial number	Text
    def get_serial(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mnfinfo get")
        jsonData = json.loads(response)
        value = jsonData['mnfinfo']['serial']
        return value, modbusVal == value
    # LAN MAC address	Text
    def get_lan_mac(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mnfinfo get")
        jsonData = json.loads(response)
        value = jsonData['mnfinfo']['mac']
        return value, modbusVal == value
    # Router name	Text
    def get_name(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mnfinfo get")
        jsonData = json.loads(response)
        value = jsonData['mnfinfo']['name']
        return value, modbusVal == value
    # Currently active SIM card slot	Text
    def get_active_sim_slot(self, modbusVal): #simX
        response = self.ssh_connection.exec_command("ubus call vuci.network.mobile mobile_status")
        jsonData = json.loads(response)
        value = ''.join(jsonData['mobile'][0]['simstate'].split()[0:2]).lower()
        return value, modbusVal == value
    # Network registration info	Text
    def get_network_registration(self, modbusVal):
        response = self.ssh_connection.exec_command("gsmctl -g")
        value = response
        return value, modbusVal == value
    # Network type	Text
    def get_network_type(self, modbusVal):
        response = self.ssh_connection.exec_command("gsmctl -t")
        value = response
        return value, modbusVal == value
    # Digital input (DIN1) state	32 bit integer
    def get_din1(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call ioman.gpio.din1 status")
        jsonData = json.loads(response)
        value = int(jsonData["value"])
        return value, modbusVal == value
    # Digital galvanically isolated input (DIN2) state	32 bit integer
    def get_din2(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call ioman.gpio.din2 status")
        jsonData = json.loads(response)
        value = int(jsonData["value"])
        return value, modbusVal == value
    # Current WAN IP address	32 bit unsigned integer
    def get_wan_ip(self, modbusVal:int): # Works only properly with WAN, mobile returns empty ipv4 field 
        responseWan = self.ssh_connection.exec_command("ubus call network.interface.wan status")
        responseMob1 = self.ssh_connection.exec_command("ubus call network.interface.mob1s1a1 status")
        responseMob2 = self.ssh_connection.exec_command("ubus call network.interface.mob1s2a1 status")
        jsonWan = json.loads(responseWan)
        jsonMob1 = json.loads(responseMob1)
        jsonMob2 = json.loads(responseMob2)
        # Multiple values should be parsed for comparrison        
        value = None
        try: value = jsonWan["ipv4-address"][0]["address"]
        except: pass
        modbusValConverted = socket.inet_ntoa(modbusVal.to_bytes(4, 'big'))
        return modbusValConverted, modbusValConverted == value
    # Analog input value	32 bit integer
    def get_analog(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call ioman.adc.adc0 status")
        jsonData = json.loads(response)
        value = int(1000*float(jsonData["value"]))
        return value, modbusVal == value
    # GPS latitude coordinate	32 bit float
    def get_gps_latitude(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call gpsd position")
        jsonData = json.loads(response)
        value = float(jsonData['latitude'])
        return value, modbusVal == value
    # GPS longitude coordinate	32 bit float
    def get_gps_longitude(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call gpsd position")
        jsonData = json.loads(response)
        value = float(jsonData['longtitude'])
        return value, modbusVal == value
    # GPS fix time	Text (Unix timestamp×1000)
    def get_gps_fixtime(self, modbusVal): ### Not implemented
        response = self.ssh_connection.exec_command("ubus call gpsd position")
        jsonData = json.loads(response)
        value = float(jsonData['timestamp'])
        return value, modbusVal == value
    # GPS date and time	Text (DDMMYYhhmmss)
    def get_gps_datetime(self, modbusVal): #### Not implemented
        response = self.ssh_connection.exec_command("") 
        value = None
        return value, True
    # GPS speed	32 bit integer
    def get_gps_speed(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call gpsd position")
        jsonData = json.loads(response)
        value = int(jsonData['speed'])
        return value, modbusVal == value
    # GPS satellite count	32 bit integer
    def get_satelites(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call gpsd position")
        jsonData = json.loads(response)
        value = int(jsonData['satellites'])
        return value, modbusVal == value
    # GPS accuracy	32 bit float
    def get_gps_accuracy(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call gpsd position")
        jsonData = json.loads(response)
        value = float(jsonData['accuracy'])
        return value, modbusVal == value
    # Mobile data received today (SIM1)	32 bit unsigned integer
    def get_data_sim1_received_day(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'day', 'sim':1, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent today (SIM1)	32 bit unsigned integer
    def get_data_sim1_sent_day(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'day', 'sim':1, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Mobile data received this week (SIM1)	32 bit unsigned integer
    def get_data_sim1_received_week(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'week', 'sim':1, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent this week (SIM1)	32 bit unsigned integer
    def get_data_sim1_sent_week(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'week', 'sim':1, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Mobile data received this month (SIM1)	32 bit unsigned integer
    def get_data_sim1_received_month(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'month', 'sim':1, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent this month (SIM1)	32 bit unsigned integer
    def get_data_sim1_sent_month(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'month', 'sim':1, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Mobile data received last 24h (SIM1)	32 bit unsigned integer
    def get_data_sim1_received_24(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'day', 'sim':1, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent last 24h (SIM1)	32 bit unsigned integer
    def get_data_sim1_sent_24(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'day', 'sim':1, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Galvanically isolated open collector output status	16 bit unsigned integer
    def get_gioc_status(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call ioman.gpio.dout2")
        jsonData = json.loads(response)
        value = jsonData["value"]
        return value, modbusVal == value
    # Relay output status	16 bit unsigned integer
    def get_relay_statys(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call ioman.relay.relay0 status")
        jsonData = json.loads(response)
        stringVar = jsonData["state"]
        value = -1
        if stringVar == 'open':
            value = 0
        elif stringVar == 'closed':
            value = 1
        return value, modbusVal == value
    # Active SIM card	16 bit unsigned integer
    def get_active_sim(self, modbusVal): # X
        response = self.ssh_connection.exec_command("ubus call vuci.network.mobile mobile_status")
        jsonData = json.loads(response)
        value = int(jsonData['mobile'][0]['simstate'].split()[1])
        return value, modbusVal == value
    # Mobile data received last week (SIM1)	32 bit unsigned integer
    def get_data_sim1_received_lastweek(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'week', 'sim':1, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent last week (SIM1)	32 bit unsigned integer
    def get_data_sim1_sent_lastweek(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'week', 'sim':1, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Mobile data received last month (SIM1)	32 bit unsigned integer
    def get_data_sim1_received_lastmonth(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'month', 'sim':1, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent last month (SIM1)	32 bit unsigned integer
    def get_data_sim1_sent_lastmonth(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'month', 'sim':1, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Mobile data received today (SIM2)	32 bit unsigned integer
    def get_data_sim2_received_today(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'day', 'sim':2, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent today (SIM2)	32 bit unsigned integer
    def get_data_sim2_sent_today(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'day', 'sim':2, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Mobile data received this week (SIM2)	32 bit unsigned integer
    def get_data_sim2_received_week(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'week', 'sim':2, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent this week (SIM2)	32 bit unsigned integer
    def get_data_sim2_sent_week(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'week', 'sim':2, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Mobile data received this month (SIM2)	32 bit unsigned integer
    def get_data_sim2_received_month(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'month', 'sim':2, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent this month (SIM2)	32 bit unsigned integer
    def get_data_sim2_sent_month(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'month', 'sim':2, 'modem':'3-1','current':true}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Mobile data received last 24h (SIM2)	32 bit unsigned integer
    def get_data_sim2_received_24(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'day', 'sim':2, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent last 24h (SIM2)	32 bit unsigned integer
    def get_data_sim2_sent_24(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'day', 'sim':2, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Mobile data received last week (SIM2)	32 bit unsigned integer
    def get_data_sim2_received_lastweek(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'week', 'sim':2, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent last week (SIM2)	32 bit unsigned integer
    def get_data_sim2_sent_lastweek(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'week', 'sim':2, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Mobile data received last month(SIM2)	32 bit unsigned integer
    def get_data_sim2_received_lastmonth(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'week', 'sim':2, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['rx'])
        return value, modbusVal == value
    # Mobile data sent last month (SIM2)	32 bit unsigned integer
    def get_data_sim2_sent_lastmonth(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call mdcollect get \"{'period':'month', 'sim':2, 'modem':'3-1','current':false}\"")
        jsonData = json.loads(response)
        value = int(jsonData['tx'])
        return value, modbusVal == value
    # Digital non-isolated input (4 PIN connector)	16 bit unsigned integer
    def get_dni(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call ioman.gpio.iio status")
        jsonData = json.loads(response)
        value = int(jsonData["value"])
        return value, modbusVal == value
    # Digital open collector output (4 PIN connector)	16 bit unsigned integer
    def get_doc(self, modbusVal):
        response = self.ssh_connection.exec_command("ubus call ioman.gpio.dout1 status")
        jsonData = json.loads(response)
        value = int(jsonData["value"])
        return value, modbusVal == value
    # IMSI	Text
    def get_imsi(self, modbusVal):
        response = self.ssh_connection.exec_command("gsmctl -x")
        value = response
        return value, modbusVal == value
