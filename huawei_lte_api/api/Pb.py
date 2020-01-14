from collections import OrderedDict
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Pb(ApiGroup):
    def get_pb_match(self, phone_number: str) -> GetResponseType:
        """
        Find number in PhoneBook
        :param phone_number:
        :return:
        """
        return self._connection.post_get('pb/pb-match', {
            'Phone': phone_number
        })

    def get_pb_list(self,
                    page: int = 1,
                    key_word: str='',
                    group_id: int=0,
                    read_count: int=50
                    ) -> GetResponseType:
        return self._connection.post_get('pb/pb-list', OrderedDict((
            ('GroupID', group_id),
            ('PageIndex', page),
            ('ReadCount', read_count),
            ('KeyWord', key_word)
        )))

    def pb_count(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.post_get('pb/pb-count')

    def group_count(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.post_get('pb/group-count')