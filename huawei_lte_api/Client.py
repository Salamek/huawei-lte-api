from huawei_lte_api.Connection import Connection
from huawei_lte_api.api.Device import Device
from huawei_lte_api.api.User import User
from huawei_lte_api.api.Monitoring import Monitoring
from huawei_lte_api.api.Security import Security
from huawei_lte_api.api.WebServer import WebServer
from huawei_lte_api.api.WLan import WLan
from huawei_lte_api.api.Cradle import Cradle
from huawei_lte_api.api.Pin import Pin
from huawei_lte_api.config.DialUp import DialUp as DialUpConfig
from huawei_lte_api.config.Global import Global
from huawei_lte_api.config.Lan import Lan as LanConfig
from huawei_lte_api.config.Network import Network as NetworkConfig
from huawei_lte_api.config.Pincode import Pincode as PincodeConfig
from huawei_lte_api.config.Sms import Sms as SmsConfig
from huawei_lte_api.config.Voice import Voice
from huawei_lte_api.config.Wifi import Wifi as WifiConfig
from huawei_lte_api.config.PcAssistant import PcAssistant
from huawei_lte_api.config.DeviceInformation import DeviceInformation
from huawei_lte_api.config.WebUICfg import WebUICfg
from huawei_lte_api.config.Device import Device as DeviceConfig
from huawei_lte_api.config.FastBoot import FastBoot
from huawei_lte_api.config.Firewall import Firewall
from huawei_lte_api.config.IPv6 import IPv6
from huawei_lte_api.config.Ota import Ota as OtaConfig
from huawei_lte_api.config.Pb import Pb as PbConfig
from huawei_lte_api.config.Sntp import Sntp
from huawei_lte_api.config.Statistic import Statistic as ConfigStatistic
from huawei_lte_api.config.Stk import Stk
from huawei_lte_api.config.Update import Update
from huawei_lte_api.config.UPnp import UPnp
from huawei_lte_api.config.Ussd import Ussd
from huawei_lte_api.config.WebSd import WebSd
from huawei_lte_api.usermanual.PublicSysResources import PublicSysResources
from huawei_lte_api.api.Ota import Ota
from huawei_lte_api.api.Net import Net
from huawei_lte_api.api.DialUp import DialUp
from huawei_lte_api.api.Sms import Sms
from huawei_lte_api.api.Redirection import Redirection
from huawei_lte_api.api.VSim import VSim
from huawei_lte_api.api.FileManager import FileManager
from huawei_lte_api.api.Dhcp import Dhcp
from huawei_lte_api.api.DDns import DDns
from huawei_lte_api.api.Diagnosis import Diagnosis
from huawei_lte_api.api.SNtp import SNtp
from huawei_lte_api.api.OnlineUpdate import OnlineUpdate
from huawei_lte_api.api.Log import Log
from huawei_lte_api.api.Time import Time
from huawei_lte_api.api.SdCard import SdCard
from huawei_lte_api.api.UsbStorage import UsbStorage
from huawei_lte_api.api.UsbPrinter import UsbPrinter
from huawei_lte_api.api.Vpn import Vpn
from huawei_lte_api.api.Ntwk import Ntwk
from huawei_lte_api.api.Global import Global as Global_
from huawei_lte_api.api.Pb import Pb
from huawei_lte_api.api.Host import Host
from huawei_lte_api.api.Language import Language
from huawei_lte_api.api.Syslog import Syslog
from huawei_lte_api.api.Voice import Voice as Voice_
from huawei_lte_api.api.Cwmp import Cwmp
from huawei_lte_api.api.Lan import Lan
from huawei_lte_api.api.Led import Led
from huawei_lte_api.api.Statistic import Statistic
from huawei_lte_api.api.TimeRule import TimeRule
from huawei_lte_api.api.Bluetooth import Bluetooth
from huawei_lte_api.api.MLog import MLog


class Client:
    def __init__(self, connection: Connection):  # pylint: disable=too-many-statements
        self.monitoring = Monitoring(connection)
        self.security = Security(connection)
        self.webserver = WebServer(connection)
        self.global_ = Global_(connection)
        self.wlan = WLan(connection)
        self.cradle = Cradle(connection)
        self.pin = Pin(connection)
        self.config_dialup = DialUpConfig(connection)
        self.config_global = Global(connection)
        self.config_lan = LanConfig(connection)
        self.config_network = NetworkConfig(connection)
        self.config_pincode = PincodeConfig(connection)
        self.config_sms = SmsConfig(connection)
        self.config_voice = Voice(connection)
        self.config_wifi = WifiConfig(connection)
        self.config_pc_assistant = PcAssistant(connection)
        self.config_device_information = DeviceInformation(connection)
        self.config_web_ui_cfg = WebUICfg(connection)
        self.config_device = DeviceConfig(connection)
        self.config_fast_boot = FastBoot(connection)
        self.config_firewall = Firewall(connection)
        self.config_ipv6 = IPv6(connection)
        self.config_ota = OtaConfig(connection)
        self.config_pb = PbConfig(connection)
        self.config_sntp = Sntp(connection)
        self.config_statistic = ConfigStatistic(connection)
        self.config_stk = Stk(connection)
        self.config_update = Update(connection)
        self.config_u_pnp = UPnp(connection)
        self.config_ussd = Ussd(connection)
        self.config_web_sd = WebSd(connection)
        self.usermanual_public_sys_resources = PublicSysResources(connection)
        self.ota = Ota(connection)
        self.net = Net(connection)
        self.dial_up = DialUp(connection)
        self.sms = Sms(connection)
        self.redirection = Redirection(connection)
        self.v_sim = VSim(connection)
        self.file_manager = FileManager(connection)
        self.dhcp = Dhcp(connection)
        self.d_dns = DDns(connection)
        self.diagnosis = Diagnosis(connection)
        self.s_ntp = SNtp(connection)
        self.user = User(connection)
        self.device = Device(connection)
        self.online_update = OnlineUpdate(connection)
        self.log = Log(connection)
        self.time = Time(connection)
        self.sd_card = SdCard(connection)
        self.usb_storage = UsbStorage(connection)
        self.usb_printer = UsbPrinter(connection)
        self.vpn = Vpn(connection)
        self.ntwk = Ntwk(connection)
        self.pb = Pb(connection)
        self.host = Host(connection)
        self.language = Language(connection)
        self.syslog = Syslog(connection)
        self.voice = Voice_(connection)
        self.cwmp = Cwmp(connection)
        self.lan = Lan(connection)
        self.led = Led(connection)
        self.statistic = Statistic(connection)
        self.timerule = TimeRule(connection)
        self.bluetooth = Bluetooth(connection)
        self.mlog = MLog(connection)
