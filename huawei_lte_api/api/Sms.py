import datetime
import dataclasses
import warnings
from collections import OrderedDict
from typing import Optional, List, Iterator

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType
from huawei_lte_api.enums.sms import BoxTypeEnum, TextModeEnum, SaveModeEnum, SendTypeEnum, PriorityEnum, TypeEnum, StatusEnum, SortTypeEnum
from huawei_lte_api.Tools import Tools


@dataclasses.dataclass
class Message:
    index: int
    status: StatusEnum
    phone: str
    content: str
    date_time: datetime.datetime
    sca: Optional[str]
    save_type: SaveModeEnum
    priority: PriorityEnum
    type: TypeEnum
    text_mode: TextModeEnum = TextModeEnum.SEVEN_BIT

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        date_time = data.get('Date')
        return Message(
            index=int(data.get('Index', 0)),
            status=StatusEnum(int(data.get('Smstat', 0))),
            phone=data.get('Phone', ''),
            content=data.get('Content', ''),
            date_time=Tools.string_to_datetime(date_time) if date_time else datetime.datetime.now(),
            sca=data.get('Sca'),
            save_type=SaveModeEnum(int(data.get('SaveType', 0))),
            priority=PriorityEnum(int(data.get('Priority', 0))),
            type=TypeEnum(int(data.get('SmsType', 0))),
        )

    def to_dict(self) -> dict:
        return {
            'Index': str(self.index),
            'Smstat': str(self.status.value),
            'Phone': self.phone,
            'Content': self.content,
            'Date': Tools.datetime_to_string(self.date_time),
            'Sca': self.sca,
            'SaveType': str(self.save_type.value),
            'Priority': str(self.priority.value),
            'SmsType': str(self.type.value)
        }


class Sms(ApiGroup):
    def get_cbsnewslist(self) -> GetResponseType:
        return self._session.get('sms/get-cbsnewslist')

    def sms_count(self) -> GetResponseType:
        return self._session.get('sms/sms-count')

    def splitinfo_sms(self) -> GetResponseType:
        return self._session.get('sms/splitinfo-sms')

    def sms_feature_switch(self) -> GetResponseType:
        return self._session.get('sms/sms-feature-switch')

    def send_status(self) -> GetResponseType:
        return self._session.get('sms/send-status')

    def get_sms_list(self,
                     page: int = 1,
                     box_type: BoxTypeEnum = BoxTypeEnum.LOCAL_INBOX,
                     read_count: int = 20,
                     sort_type: SortTypeEnum = SortTypeEnum.DATE,
                     ascending: bool = False,
                     unread_preferred: bool = False
                     ) -> GetResponseType:

        if isinstance(sort_type, int):
            warnings.warn(
                "get_sms_list: Passing int into sort_type is deprecated and will be removed in next minor version! Please use enums.sms.SortTypeEnum instead!.",
                DeprecationWarning
            )
            sort_type = SortTypeEnum(sort_type)

        # Note: at least the B525s-23a is order sensitive
        return self._session.post_get('sms/sms-list', OrderedDict((
            ('PageIndex', page),
            ('ReadCount', read_count),
            ('BoxType', box_type.value),
            ('SortType', sort_type.value),
            ('Ascending', 1 if ascending else 0),
            ('UnreadPreferred', 1 if unread_preferred else 0),
        )))

    def delete_sms(self, sms_id: int) -> SetResponseType:
        """
        Delete single SMS by its ID
        :param sms_id: Id of SMS you wish to delete
        :return: dict
        """
        return self._session.post_set('sms/delete-sms', {'Index': sms_id})

    def backup_sim(self, from_date: datetime.datetime, is_move: bool = False) -> SetResponseType:
        return self._session.post_set('sms/backup-sim', OrderedDict((
            ('IsMove', int(is_move)),
            ('Date', Tools.datetime_to_string(from_date))
        )))

    def set_read(self, sms_id: int) -> SetResponseType:
        return self._session.post_set('sms/set-read', {
            'Index': sms_id
        })

    def save_sms(self,
                 phone_numbers: List[str],
                 message: str,
                 sms_index: int = -1,
                 sca: str = '',
                 text_mode: TextModeEnum = TextModeEnum.SEVEN_BIT,
                 from_date: Optional[datetime.datetime] = None,
                 ) -> SetResponseType:

        if from_date is None:
            from_date = datetime.datetime.utcnow()

        return self._session.post_set('sms/save-sms', OrderedDict((
            ('Index', sms_index),
            ('Phones', {'Phone': phone_numbers}),
            ('Sca', sca),
            ('Content', message),
            ('Length', len(message)),
            ('Reserved', text_mode.value),
            ('Date', Tools.datetime_to_string(from_date))
        )))

    def send_sms(self,
                 phone_numbers: List[str],
                 message: str,
                 sms_index: int = -1,
                 sca: str = '',
                 text_mode: TextModeEnum = TextModeEnum.SEVEN_BIT,
                 from_date: Optional[datetime.datetime] = None,
                 ) -> SetResponseType:

        if from_date is None:
            from_date = datetime.datetime.utcnow()
        return self._session.post_set('sms/send-sms', OrderedDict((
            ('Index', sms_index),
            ('Phones', {'Phone': phone_numbers}),
            ('Sca', sca),
            ('Content', message),
            ('Length', len(message)),
            ('Reserved', text_mode.value),
            ('Date', Tools.datetime_to_string(from_date))
        )))

    def cancel_send(self) -> SetResponseType:
        return self._session.post_set('sms/cancel-send', 1)

    def config(self) -> GetResponseType:
        return self._session.get('sms/config')

    def set_config(self,
                   sca: str,
                   save_mode: SaveModeEnum = SaveModeEnum.LOCAL,
                   validity: int = 10752,
                   use_s_report: bool = False,
                   send_type: SendTypeEnum = SendTypeEnum.SEND,
                   priority: PriorityEnum = PriorityEnum.NORMAL
                   ) -> SetResponseType:
        return self._session.post_set('sms/config', OrderedDict((
            ('SaveMode', save_mode.value),
            ('Validity', validity),
            ('Sca', sca),
            ('UseSReport', use_s_report),
            ('SendType', send_type.value),
            ('Priority', priority.value)
        )))

    def sms_count_contact(self) -> GetResponseType:
        return self._session.get('sms/sms-count-contact')

    def sms_list_contact(self,
                         pageindex: int = 1,
                         readcount: int = 20,
                         ) -> GetResponseType:
        return self._session.post_get('sms/sms-list-contact', {
            'pageindex': pageindex,
            'readcount': readcount,
        })

    def get_sms_list_pdu(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.post_get('sms/sms-list-pdu')

    def split_sms(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('sms/split-sms')

    def send_sms_pdu(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('sms/send-sms-pdu')

    def recover_sms(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('sms/recover-sms')

    def copy_sms(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('sms/copy-sms')

    def move_sms(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('sms/move-sms')

    def get_messages(self,
                     page: int = 1,
                     box_type: BoxTypeEnum = BoxTypeEnum.LOCAL_INBOX,
                     read_count: Optional[int] = None,
                     sort_type: SortTypeEnum = SortTypeEnum.DATE,
                     ascending: bool = False,
                     unread_preferred: bool = False
                     ) -> Iterator[Message]:

        # No read count, return all, API does not provide a way to return all so we need to do it our self
        if read_count is None:
            read_count = 20  # Read by chunks of 20
            page = 1  # Start page has to be always 1

        while True:
            now = datetime.datetime.now()
            sms_list_tmp = Tools.enforce_list_response(self.get_sms_list(page, box_type, read_count, sort_type, ascending, unread_preferred), 'Message', 'Messages')
            if int(sms_list_tmp.get('Count', 0)) == 0:
                break

            # get messages
            for message_raw in sms_list_tmp.get('Messages', {}).get('Message', []):
                message = Message.from_dict(message_raw)

                # Check if message is possibly multipart,
                # if it is ignore it if is younger then 60 seconds
                # This way we provide the router with enough time to receive all possible parts and do correct rebuild
                if message.type == TypeEnum.MULTIPART and message.date_time + datetime.timedelta(seconds=10) > now:
                    continue

                yield message

            page += 1
