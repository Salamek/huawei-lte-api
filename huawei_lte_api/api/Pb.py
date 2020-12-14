from collections import OrderedDict
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType, SetResponseType


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
                    read_count: int=50,
                    save_type: int=0,
                    sort_type: int=1,
                    ascending: int=1
                    ) -> GetResponseType:
        return self._connection.post_get('pb/pb-list', OrderedDict((
            ('GroupID', group_id),
            ('PageIndex', page),
            ('ReadCount', read_count),
            ('SaveType', save_type),
            ('SortType', sort_type),
            ('Ascending', ascending), 
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


    def pb_new( self, 
                group_id: int=0,
                save_type: int=0,
                name: str='', 
                mobile_phone: str='', 
                home_phone: str='', 
                work_phone: str='', 
                work_email: str='') -> SetResponseType:
        """
        Add new entry to global PhoneBook
        :param
        :return:
        """
        class Node:
            def __init__(self, name):
                self._name = name

            def __str__(self):
                return self._name

        data = OrderedDict([
            ('GroupID',  group_id),
            ('SaveType', save_type),
            (Node('Field'), {
                'Name': 'FormattedName',
                'Value': name
            }),
            (Node('Field'), {
                'Name': 'MobilePhone',
                'Value': mobile_phone
            }),
            (Node('Field'), {
                'Name': 'HomePhone',
                'Value': home_phone
            }),
            (Node('Field'), {
                'Name': 'WorkPhone',
                'Value': work_phone
            }),
            (Node('Field'), {
                'Name': 'WorkEmail',
                'Value': work_email
            }),
        ])

        dicttoxml_xargs = {
            'attr_type': False
        }

        return self._connection.post_set('pb/pb-new', data, dicttoxml_xargs=dicttoxml_xargs)

    def pb_delete(self, pb_index: int) -> SetResponseType:
        """
        Delete single PB Item by its ID
        :param pb_index: Id of PB Item you wish to delete
        :return: dict
        """
        return self._connection.post_set('pb/pb-delete', {'Index': pb_index})

    def group_delete(self, group_id: int) -> SetResponseType:
        """
        Delete Phonebook group by its ID
        :param group_id: Id of Group you wish to delete
        :return:
        """
        return self._connection.post_set('pb/group-delete', {'GroupID': group_id})

    def group_list(self,
                    page: int = 1,
                    read_count: int=50,
                    sort_type: int=1,
                    ascending: int=1
                    ) -> GetResponseType:
        return self._connection.post_get('pb/group-list', OrderedDict((
            ('PageIndex', page),
            ('ReadCount', read_count),
            ('SortType', sort_type),
            ('Ascending', ascending)
        )))

    def group_new(self, name_str: str) -> SetResponseType:
        """
        Create new Phonebook group by its name
        :param name_str: name of PB Group you wish to delete
        :return:
        """
        return self._connection.post_set('pb/group-new', {'GroupName': name_str})

# missing functions
#
# pb/group-update
# pb/pb-copySIM
# pb/pb-export
# pb/pb-import
# pb/pb-import-field
# pb/pb-import-length
# pb/pb-import-match
# pb/pb-update
# pb/pb-move
# pb/pb-match
