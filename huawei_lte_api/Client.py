from huawei_lte_api.Connection import Connection
from huawei_lte_api.api.Device import Device
from huawei_lte_api.api.User import User
from huawei_lte_api.api.Monitoring import Monitoring
from huawei_lte_api.api.Security import Security
from huawei_lte_api.api.WebServer import WebServer
from huawei_lte_api.api.WLan import WLan
from huawei_lte_api.api.Cradle import Cradle
from huawei_lte_api.api.Pin import Pin
from huawei_lte_api.config.Global import Global
from huawei_lte_api.config.Voice import Voice
from huawei_lte_api.config.PcAssistant import PcAssistant
from huawei_lte_api.config.DeviceInformation import DeviceInformation
from huawei_lte_api.config.WebUICfg import WebUICfg
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


class Client:
    def __init__(self, connection: Connection):
        self.monitoring = Monitoring(connection)
        self.security = Security(connection)
        self.webserver = WebServer(connection)
        self.global_ = Global_(connection)
        self.wlan = WLan(connection)
        self.cradle = Cradle(connection)
        self.pin = Pin(connection)
        self.config_global = Global(connection)
        self.config_voice = Voice(connection)
        self.config_pc_assistant = PcAssistant(connection)
        self.config_device_information = DeviceInformation(connection)
        self.config_web_ui_cfg = WebUICfg(connection)
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
