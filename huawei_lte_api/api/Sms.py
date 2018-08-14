import datetime
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call
from huawei_lte_api.enums.sms import BoxTypeEnum, TextModeEnum, SaveModeEnum, SendTypeEnum, PriorityEnum


class Sms(ApiGroup):
    def get_cbsnewslist(self) -> dict:
        return self._connection.get('sms/get-cbsnewslist')

    def sms_count(self) -> dict:
        return self._connection.get('sms/sms-count')

    def splitinfo_sms(self) -> dict:
        return self._connection.get('sms/splitinfo-sms')

    @authorized_call
    def sms_feature_switch(self) -> dict:
        return self._connection.get('sms/sms-feature-switch')

    def send_status(self) -> dict:
        return self._connection.get('sms/send-status')

    def get_sms_list(self,
                     page: int=1,
                     box_type: BoxTypeEnum=BoxTypeEnum.LOCAL_INBOX,
                     read_count: int=None,
                     sort_type: int=0,
                     ascending: int=0,
                     unread_preferred: int=0
                     ) -> dict:
        return self._connection.post('sms/sms-list', {
            'PageIndex': page,
            'BoxType': box_type.value,
            'ReadCount': read_count,
            'SortType': sort_type,
            'Ascending': ascending,
            'UnreadPreferred': unread_preferred
        })

    def delete_sms(self, sms_ids: list):
        data = []
        for sms_id in sms_ids:
            data.append({'Index': sms_id})
        return self._connection.post('sms/delete-sms', data)

    def backup_sim(self, from_date: datetime.datetime, is_move: bool=False):
        return self._connection.post('sms/backup-sim', {
            'IsMove': int(is_move),
            'Date': from_date.strftime("%Y-%m-%d %H:%M:%S")
        })

    def set_read(self, sms_id: int):
        return self._connection.post('sms/set-read', {
            'Index': sms_id
        })

    @authorized_call
    def save_sms(self,
                 phone_numbers: list,
                 message: str,
                 sms_index: int=-1,
                 sca: str='',
                 text_mode: TextModeEnum=TextModeEnum.SEVEN_BIT,
                 from_date: datetime.datetime=datetime.datetime.utcnow()
                 ):

        dicttoxml_xargs = {
            'item_func': lambda x: x[:-1]
        }

        return self._connection.post('sms/save-sms', {
            'Index': sms_index,
            'Phones':  phone_numbers,
            'Sca': sca,
            'Content': message,
            'Length': len(message),
            'Reserved': text_mode.value,
            'Date': from_date.strftime("%Y-%m-%d %H:%M:%S")
        }, dicttoxml_xargs=dicttoxml_xargs)

    @authorized_call
    def send_sms(self,
                 phone_numbers: list,
                 message: str,
                 sms_index: int=-1,
                 sca: str='',
                 text_mode: TextModeEnum=TextModeEnum.SEVEN_BIT,
                 from_date: datetime.datetime=datetime.datetime.utcnow()
                 ):

        dicttoxml_xargs = {
            'item_func': lambda x: x[:-1]
        }

        return self._connection.post('sms/send-sms', {
            'Index': sms_index,
            'Phones': phone_numbers,
            'Sca': sca,
            'Content': message,
            'Length': len(message),
            'Reserved': text_mode.value,
            'Date': from_date.strftime("%Y-%m-%d %H:%M:%S")
        }, dicttoxml_xargs=dicttoxml_xargs)

    def cancel_send(self):
        return self._connection.post('sms/cancel-send', 1)

    @authorized_call
    def config(self) -> dict:
        return self._connection.get('sms/config')

    @authorized_call
    def set_config(self,
                   sca: str,
                   save_mode: SaveModeEnum=SaveModeEnum.LOCAL,
                   validity: int=10752,
                   use_s_report: bool=False,
                   send_type: SendTypeEnum=SendTypeEnum.SEND,
                   priority: PriorityEnum=PriorityEnum.NORMAL
                   ):
        return self._connection.post('sms/config', {
            'SaveMode': save_mode.value,
            'Validity': validity,
            'Sca': sca,
            'UseSReport': use_s_report,
            'SendType': send_type.value,
            'Priority': priority.value
        })