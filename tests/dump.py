#!/usr/bin/env python3

from argparse import ArgumentParser
import os.path
import pprint
import sys
from typing import Any, Callable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))

from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection


parser = ArgumentParser()
parser.add_argument('url', type=str)
parser.add_argument('--username', type=str)
parser.add_argument('--password', type=str)
args = parser.parse_args()

if args.username is None:
    connection = Connection(args.url)
else:
    connection = AuthorizedConnection(
        args.url, username=args.username, password=args.password)

client = Client(connection)

def dump(method: Callable[[], Any]) -> None:
    print("==== %s" % method)
    try:
        pprint.pprint(method())
    except Exception as e:
        print(str(e))
    print("")

dump(client.device.information)
dump(client.device.autorun_version)
dump(client.device.device_feature_switch)
dump(client.device.basic_information)
dump(client.device.basicinformation)
dump(client.device.usb_tethering_switch)
dump(client.device.boot_time)
dump(client.device.signal)
dump(client.device.antenna_status)
dump(client.device.antenna_type)
dump(client.device.logsetting)

dump(client.user.state_login)
dump(client.user.remind)
dump(client.user.password)
dump(client.user.pwd)
dump(client.user.authentication_login)
dump(client.user.challenge_login)
dump(client.user.hilink_login)
dump(client.user.history_login)
dump(client.user.heartbeat)
dump(client.user.web_feature_switch)
dump(client.user.screen_state)
dump(client.user.session)

dump(client.monitoring.converged_status)
dump(client.monitoring.status)
dump(client.monitoring.check_notifications)
dump(client.monitoring.traffic_statistics)
dump(client.monitoring.start_date)
dump(client.monitoring.start_date_wlan)
dump(client.monitoring.month_statistics)
dump(client.monitoring.month_statistics_wlan)
dump(client.monitoring.wifi_month_setting)

dump(client.security.bridgemode)
dump(client.security.get_firewall_switch)
dump(client.security.mac_filter)
dump(client.security.lan_ip_filter)
dump(client.security.virtual_servers)
dump(client.security.url_filter)
dump(client.security.upnp)
dump(client.security.dmz)
dump(client.security.sip)
dump(client.security.feature_switch)
dump(client.security.nat)
dump(client.security.special_applications)
dump(client.security.white_lan_ip_filter)
dump(client.security.white_url_filter)
dump(client.security.acls)

dump(client.webserver.publickey)
dump(client.webserver.token)
dump(client.webserver.white_list_switch)

dump(client.global_.module_switch)

dump(client.wlan.wifi_feature_switch)
dump(client.wlan.station_information)
dump(client.wlan.basic_settings)
dump(client.wlan.security_settings)
dump(client.wlan.multi_security_settings)
dump(client.wlan.multi_security_settings_ex)
dump(client.wlan.multi_basic_settings)
dump(client.wlan.host_list)
dump(client.wlan.handover_setting)
dump(client.wlan.multi_switch_settings)
dump(client.wlan.multi_macfilter_settings)
dump(client.wlan.multi_macfilter_settings_ex)
dump(client.wlan.mac_filter)
dump(client.wlan.oled_showpassword)
dump(client.wlan.wps)
dump(client.wlan.wps_appin)
dump(client.wlan.wps_pbc)
dump(client.wlan.wps_switch)
dump(client.wlan.status_switch_settings)
dump(client.wlan.wifiprofile)
dump(client.wlan.wififrequence)
dump(client.wlan.wifiscanresult)

dump(client.cradle.status_info)
dump(client.cradle.feature_switch)
dump(client.cradle.basic_info)
dump(client.cradle.factory_mac)
dump(client.cradle.mac_info)

dump(client.pin.status)
dump(client.pin.simlock)
dump(client.pin.save_pin)

dump(client.language.current_language)

dump(client.config_device_information.config)

dump(client.config_dialup.config)
dump(client.config_dialup.connectmode)
dump(client.config_dialup.profileswitch)
dump(client.config_dialup.lmt_auto_mode_disconnect)

dump(client.config_global.languagelist)
dump(client.config_global.config)
dump(client.config_global.net_type)

dump(client.config_lan.config)

dump(client.config_network.config)
dump(client.config_network.net_mode)
dump(client.config_network.networkmode)
dump(client.config_network.networkband_null)

dump(client.config_pc_assistant.config)
dump(client.config_pc_assistant.updateautorun)

dump(client.config_pincode.config)

dump(client.config_sms.config)

dump(client.config_voice.config)

dump(client.config_web_ui_cfg.config)

dump(client.config_wifi.configure)
dump(client.config_wifi.country_channel)
dump(client.config_wifi.channel_auto_match_hardware)

dump(client.config_device.config)

dump(client.config_fast_boot.config)

dump(client.config_firewall.config)

dump(client.config_ipv6.config)

dump(client.config_ota.config)

dump(client.config_pb.config)

dump(client.config_sntp.config)

dump(client.config_statistic.config)

dump(client.config_stk.config)

dump(client.config_update.config)

dump(client.config_u_pnp.config)

dump(client.config_ussd.prepaidussd)
dump(client.config_ussd.postpaidussd)

dump(client.config_web_sd.config)

dump(client.usermanual_public_sys_resources.config)

dump(client.ota.status)

dump(client.net.current_plmn)
dump(client.net.net_mode)
dump(client.net.network)
dump(client.net.register)
dump(client.net.net_mode_list)
# DoS? dump(client.net.plmn_list)
dump(client.net.net_feature_switch)
dump(client.net.cell_info)
dump(client.net.csps_state)

dump(client.dial_up.mobile_dataswitch)
dump(client.dial_up.connection)
dump(client.dial_up.dialup_feature_switch)
dump(client.dial_up.profiles)
dump(client.dial_up.auto_apn)

dump(client.sms.get_cbsnewslist)
dump(client.sms.sms_count)
dump(client.sms.send_status)
dump(client.sms.get_sms_list)
dump(client.sms.config)
dump(client.sms.sms_count_contact)
dump(client.sms.get_sms_list_pdu)

dump(client.redirection.homepage)

dump(client.v_sim.operateswitch_vsim)

dump(client.dhcp.settings)
dump(client.dhcp.feature_switch)
dump(client.dhcp.dhcp_host_info)
dump(client.dhcp.static_addr_info)

dump(client.d_dns.get_ddns_list)
dump(client.d_dns.get_status)

dump(client.diagnosis.trace_route_result)
dump(client.diagnosis.diagnose_ping)
dump(client.diagnosis.diagnose_traceroute)
dump(client.diagnosis.time_reboot)

dump(client.s_ntp.get_settings)
dump(client.s_ntp.sntpswitch)
dump(client.s_ntp.serverinfo)
dump(client.s_ntp.timeinfo)

dump(client.online_update.check_new_version)
dump(client.online_update.status)
dump(client.online_update.url_list)
dump(client.online_update.ack_newversion)
# May cause device reboot: dump(client.online_update.cancel_downloading)
dump(client.online_update.upgrade_messagebox)
dump(client.online_update.configuration)
dump(client.online_update.autoupdate_config)
dump(client.online_update.redirect_cancel)

dump(client.log.loginfo)

dump(client.time.timeout)

dump(client.sd_card.dlna_setting)
dump(client.sd_card.sdcard)
dump(client.sd_card.sdcardsamba)
dump(client.sd_card.printerlist)
dump(client.sd_card.share_account)

dump(client.usb_storage.fsstatus)
dump(client.usb_storage.usbaccount)

dump(client.usb_printer.printerlist)

dump(client.vpn.feature_switch)
dump(client.vpn.br_list)
dump(client.vpn.ipsec_settings)
dump(client.vpn.l2tp_settings)
dump(client.vpn.pptp_settings)
dump(client.vpn.status)

dump(client.ntwk.lan_upnp_portmapping)
dump(client.ntwk.celllock)

dump(client.pb.get_pb_list)
dump(client.pb.pb_count)
dump(client.pb.group_count)

dump(client.syslog.querylog)

dump(client.voice.featureswitch)
dump(client.voice.sipaccount)
dump(client.voice.sipadvance)
dump(client.voice.sipserver)
dump(client.voice.speeddial)
dump(client.voice.functioncode)
dump(client.voice.voiceadvance)
dump(client.voice.codec)

dump(client.cwmp.basic_info)

dump(client.lan.host_info)

dump(client.led.nightmode)

dump(client.statistic.feature_roam_statistic)

dump(client.timerule.timerule)

dump(client.bluetooth.settings)
dump(client.bluetooth.scan)

dump(client.mlog.mobile_logger)

dump(client.voice.voicebusy)

if isinstance(connection, AuthorizedConnection):
    client.user.logout()
