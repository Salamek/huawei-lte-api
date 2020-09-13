import datetime
from collections import OrderedDict
from typing import Optional
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType, SetResponseType
from huawei_lte_api.enums.sms import BoxTypeEnum, TextModeEnum, SaveModeEnum, SendTypeEnum, PriorityEnum


class Sms(ApiGroup):
    def get_cbsnewslist(self) -> GetResponseType:
        return self._connection.get('sms/get-cbsnewslist')

    def sms_count(self) -> GetResponseType:
        return self._connection.get('sms/sms-count')

    def splitinfo_sms(self) -> GetResponseType:
        return self._connection.get('sms/splitinfo-sms')

    def sms_feature_switch(self) -> GetResponseType:
        return self._connection.get('sms/sms-feature-switch')

    def send_status(self) -> GetResponseType:
        return self._connection.get('sms/send-status')

    def get_sms_list(self,
                     page: int=1,
                     box_type: BoxTypeEnum=BoxTypeEnum.LOCAL_INBOX,
                     read_count: int=20,
                     sort_type: int=0,
                     ascending: int=0,
                     unread_preferred: int=0
                     ) -> GetResponseType:
        # Note: at least the B525s-23a is order sensitive
        return self._connection.post_get('sms/sms-list', OrderedDict((
            ('PageIndex', page),
            ('ReadCount', read_count),
            ('BoxType', box_type.value),
            ('SortType', sort_type),
            ('Ascending', ascending),
            ('UnreadPreferred', unread_preferred),
        )))

    def delete_sms(self, sms_id: int) -> SetResponseType:
        """
        Delete single SMS by its ID
        :param sms_id: Id of SMS you wish to delete
        :return: dict
        """
        return self._connection.post_set('sms/delete-sms', {'Index': sms_id})

    def backup_sim(self, from_date: datetime.datetime, is_move: bool=False) -> SetResponseType:
        return self._connection.post_set('sms/backup-sim', OrderedDict((
            ('IsMove', int(is_move)),
            ('Date', from_date.strftime("%Y-%m-%d %H:%M:%S"))
        )))

    def set_read(self, sms_id: int) -> SetResponseType:
        return self._connection.post_set('sms/set-read', {
            'Index': sms_id
        })

    def save_sms(self,
                 phone_numbers: list,
                 message: str,
                 sms_index: int=-1,
                 sca: str='',
                 text_mode: TextModeEnum=TextModeEnum.SEVEN_BIT,
                 from_date: Optional[datetime.datetime]=None,
                 ) -> SetResponseType:

        if from_date is None:
            from_date = datetime.datetime.utcnow()
        dicttoxml_xargs = {
            'item_func': lambda x: x[:-1]
        }

        return self._connection.post_set('sms/save-sms', OrderedDict((
            ('Index', sms_index),
            ('Phones',  phone_numbers),
            ('Sca', sca),
            ('Content', message),
            ('Length', len(message)),
            ('Reserved', text_mode.value),
            ('Date', from_date.strftime("%Y-%m-%d %H:%M:%S"))
        )), dicttoxml_xargs=dicttoxml_xargs)

    def send_sms(self,
                 phone_numbers: list,
                 message: str,
                 sms_index: int=-1,
                 sca: str='',
                 text_mode: TextModeEnum=TextModeEnum.SEVEN_BIT,
                 from_date: Optional[datetime.datetime]=None,
                 ) -> SetResponseType:

        if from_date is None:
            from_date = datetime.datetime.utcnow()
        dicttoxml_xargs = {
            'item_func': lambda x: x[:-1]
        }

        return self._connection.post_set('sms/send-sms', OrderedDict((
            ('Index', sms_index),
            ('Phones', phone_numbers),
            ('Sca', sca),
            ('Content', message),
            ('Length', len(message)),
            ('Reserved', text_mode.value),
            ('Date', from_date.strftime("%Y-%m-%d %H:%M:%S"))
        )), dicttoxml_xargs=dicttoxml_xargs)

    def cancel_send(self) -> SetResponseType:
        return self._connection.post_set('sms/cancel-send', {
            'request': 1,
        }, dicttoxml_xargs={
            'root': False,
        })

    def config(self) -> GetResponseType:
        return self._connection.get('sms/config')

    def set_config(self,
                   sca: str,
                   save_mode: SaveModeEnum=SaveModeEnum.LOCAL,
                   validity: int=10752,
                   use_s_report: bool=False,
                   send_type: SendTypeEnum=SendTypeEnum.SEND,
                   priority: PriorityEnum=PriorityEnum.NORMAL
                   ) -> SetResponseType:
        return self._connection.post_set('sms/config', OrderedDict((
            ('SaveMode', save_mode.value),
            ('Validity', validity),
            ('Sca', sca),
            ('UseSReport', use_s_report),
            ('SendType', send_type.value),
            ('Priority', priority.value)
        )))

    def sms_count_contact(self) -> GetResponseType:
        return self._connection.get('sms/sms-count-contact')

    def get_sms_list_pdu(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('sms/sms-list-pdu')

    def split_sms(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('sms/split-sms')

    def send_sms_pdu(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('sms/send-sms-pdu')

    def recover_sms(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('sms/recover-sms')

    def copy_sms(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('sms/copy-sms')

    def move_sms(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('sms/move-sms')
