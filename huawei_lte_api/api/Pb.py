
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Pb(ApiGroup):
    def get_pb_match(self, phone_number: str) -> dict:
        """
    Find number in PhoneBook
    :param phone_number:
    :return:
    """
        return self._connection.post('pb/pb-match', {
            'Phone': phone_number
        })

    def get_pb_list(self,
                    page: int = 1,
                    key_word: str='',
                    group_id: int=0,
                    read_count: int=50
                    ) -> dict:
        return self._connection.post('pb/pb-list', {
            'GroupID': group_id,
            'PageIndex': page,
            'ReadCount': read_count,
            'KeyWord': key_word
        })