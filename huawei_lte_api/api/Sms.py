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
    index: int  # Index in API
    status: StatusEnum  # Status of SMS
    phone: str  # Phone number of sender
    content: str  # Text content of SMS
    date_time: datetime.datetime  # Datetime of SMS send/receive
    sca: Optional[str]  # Message center number in INTL format eg. +420603052000
    save_type: SaveModeEnum  # How to save received SMS in device
    priority: PriorityEnum  # What priority this SMS have
    type: TypeEnum  # Type of SMS
    text_mode: TextModeEnum = TextModeEnum.SEVEN_BIT  # Type of encoding of SMS

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
        return Tools.enforce_list_response(self._session.post_get('sms/sms-list', OrderedDict((
            ('PageIndex', page),
            ('ReadCount', read_count),
            ('BoxType', box_type.value),
            ('SortType', sort_type.value),
            ('Ascending', 1 if ascending else 0),
            ('UnreadPreferred', 1 if unread_preferred else 0),
        ))), 'Message', 'Messages')

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
                 sca: Optional[str] = None,
                 text_mode: TextModeEnum = TextModeEnum.SEVEN_BIT,
                 from_date: Optional[datetime.datetime] = None,
                 ) -> SetResponseType:
        """

        :param phone_numbers:
        :param message:
        :param sms_index:
        :param sca: (Optional) Message center number in INTL format eg. +420603052000
        :param text_mode:
        :param from_date:
        :return:
        """

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
                 sca: Optional[str] = None,
                 text_mode: TextModeEnum = TextModeEnum.SEVEN_BIT,
                 from_date: Optional[datetime.datetime] = None,
                 ) -> SetResponseType:
        """

        :param phone_numbers:
        :param message:
        :param sms_index:
        :param sca: (Optional) Message center number in INTL format eg. +420603052000
        :param text_mode:
        :param from_date:
        :return:
        """
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
        """
        Sets default SMS send config
        :param sca: Message center number in INTL format eg. +420603052000
        :param save_mode:
        :param validity: validity in seconds?
        :param use_s_report:
        :param send_type:
        :param priority:
        :return:
        """
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

    def get_sms_list_pdu(self,
                         page: int = 1,
                         box_type: BoxTypeEnum = BoxTypeEnum.LOCAL_INBOX,
                         read_count: int = 20,
                         ) -> GetResponseType:
        """
        Return SMS in PDU format
        :param page: page number
        :param box_type: box type
        :param read_count: items per page
        :return:
        """
        return self._session.post_get('sms/sms-list-pdu', {
            'PageIndex': page,
            'ReadCount': read_count,
            'BoxType': box_type.value,
        })

    def split_sms(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('sms/split-sms')

    def send_sms_pdu(self,
                     pdu: str,
                     length: int,
                     sms_index: int = -1,
                     sca: Optional[str] = None,
                     validity: int = 10752,
                     status_report: bool = False,
                     save_mode: SaveModeEnum = SaveModeEnum.LOCAL,
                     send_type: SendTypeEnum = SendTypeEnum.SEND
                     ) -> SetResponseType:
        """
        Sends PDU SMS, this is not implemented on my router so not tested
        :param pdu: PDU to send e.g. 001100098121436587F900000B05E8329BFD06
        :param length: !TODO Length of PDU not an actual len() but some magic calculation I will not research right now
        :param sms_index: Index of sms in router default -1
        :param sca: # Message center number in INTL format e.g. +420603052000
        :param validity: validity in seconds?
        :param status_report: Require status report for sms (received or not)
        :param save_mode: SaveModeEnum
        :param send_type: SendTypeEnum
        :return:
        """

        return self._session.post_set('sms/send-sms-pdu', {
            'Index': sms_index,
            'PDU': pdu,
            'Length': length,
            'SaveMode': save_mode.value,
            'Validity': validity,  # validity in seconds?
            'Sca': sca,  # Message center number in INTL format eg. +420603052000
            'UseSReport': 1 if status_report else 0,  # Report SMS received
            'SendType': send_type.value
        })

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
            sms_list_tmp = self.get_sms_list(page, box_type, read_count, sort_type, ascending, unread_preferred)
            if int(sms_list_tmp.get('Count', 0)) == 0:
                break

            # get messages
            for message_raw in sms_list_tmp.get('Messages', {}).get('Message', []):
                message = Message.from_dict(message_raw)

                # Check if message is possibly multipart,
                # if it is ignore it if is younger than 60 seconds
                # This way we provide the router with enough time to receive all possible parts and do correct rebuild
                if message.type == TypeEnum.MULTIPART and message.date_time + datetime.timedelta(seconds=10) > now:
                    continue

                yield message

            page += 1
