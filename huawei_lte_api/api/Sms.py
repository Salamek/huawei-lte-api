import datetime
from collections import OrderedDict
from typing import Optional
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.enums.sms import BoxTypeEnum, TextModeEnum, SaveModeEnum, SendTypeEnum, PriorityEnum


class Sms(ApiGroup):
    def get_cbsnewslist(self) -> dict:
        return self._connection.get('sms/get-cbsnewslist')

    def sms_count(self) -> dict:
        return self._connection.get('sms/sms-count')

    def splitinfo_sms(self) -> dict:
        return self._connection.get('sms/splitinfo-sms')

    def sms_feature_switch(self) -> dict:
        return self._connection.get('sms/sms-feature-switch')

    def send_status(self) -> dict:
        return self._connection.get('sms/send-status')

    def get_sms_list(self,
                     page: int=1,
                     box_type: BoxTypeEnum=BoxTypeEnum.LOCAL_INBOX,
                     read_count: int=20,
                     sort_type: int=0,
                     ascending: int=0,
                     unread_preferred: int=0
                     ) -> dict:
        # Note: at least the B525s-23a is order sensitive
        return self._connection.post('sms/sms-list', OrderedDict((
            ('PageIndex', page),
            ('ReadCount', read_count),
            ('BoxType', box_type.value),
            ('SortType', sort_type),
            ('Ascending', ascending),
            ('UnreadPreferred', unread_preferred),
        )))

    def delete_sms(self, sms_ids: list):
        data = []
        for sms_id in sms_ids:
            data.append({'Index': sms_id})
        return self._connection.post('sms/delete-sms', data)

    def backup_sim(self, from_date: datetime.datetime, is_move: bool=False):
        return self._connection.post('sms/backup-sim', OrderedDict((
            ('IsMove', int(is_move)),
            ('Date', from_date.strftime("%Y-%m-%d %H:%M:%S"))
        )))

    def set_read(self, sms_id: int):
        return self._connection.post('sms/set-read', {
            'Index': sms_id
        })

    def save_sms(self,
                 phone_numbers: list,
                 message: str,
                 sms_index: int=-1,
                 sca: str='',
                 text_mode: TextModeEnum=TextModeEnum.SEVEN_BIT,
                 from_date: Optional[datetime.datetime]=None,
                 ):

        if from_date is None:
            from_date = datetime.datetime.utcnow()
        dicttoxml_xargs = {
            'item_func': lambda x: x[:-1]
        }

        return self._connection.post('sms/save-sms', OrderedDict((
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
                 ):

        if from_date is None:
            from_date = datetime.datetime.utcnow()
        dicttoxml_xargs = {
            'item_func': lambda x: x[:-1]
        }

        return self._connection.post('sms/send-sms', OrderedDict((
            ('Index', sms_index),
            ('Phones', phone_numbers),
            ('Sca', sca),
            ('Content', message),
            ('Length', len(message)),
            ('Reserved', text_mode.value),
            ('Date', from_date.strftime("%Y-%m-%d %H:%M:%S"))
        )), dicttoxml_xargs=dicttoxml_xargs)

    def cancel_send(self):
        return self._connection.post('sms/cancel-send', {
            'request': 1,
        }, dicttoxml_xargs={
            'root': False,
        })

    def config(self) -> dict:
        return self._connection.get('sms/config')

    def set_config(self,
                   sca: str,
                   save_mode: SaveModeEnum=SaveModeEnum.LOCAL,
                   validity: int=10752,
                   use_s_report: bool=False,
                   send_type: SendTypeEnum=SendTypeEnum.SEND,
                   priority: PriorityEnum=PriorityEnum.NORMAL
                   ):
        return self._connection.post('sms/config', OrderedDict((
            ('SaveMode', save_mode.value),
            ('Validity', validity),
            ('Sca', sca),
            ('UseSReport', use_s_report),
            ('SendType', send_type.value),
            ('Priority', priority.value)
        )))

    def sms_count_contact(self) -> dict:
        return self._connection.get('sms/sms-count-contact')
