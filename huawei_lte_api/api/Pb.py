from collections import OrderedDict

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType


class Pb(ApiGroup):
    def get_pb_match(self, phone_number: str) -> GetResponseType:
        """
        Find number in PhoneBook

        :param phone_number: Phone number to search for.
        :return: Matching phone book entry.

        Usage example:
        >>> pb = Pb(session)
        >>> match = pb.get_pb_match(phone_number="123456789")
        >>> print(match)
        """
        return self._session.post_get('pb/pb-match', {
            'Phone': phone_number
        })

    def get_pb_list(self,
                    page: int = 1,
                    key_word: str = '',
                    group_id: int = 0,
                    read_count: int = 50,
                    save_type: int = 0,
                    sort_type: int = 1,
                    ascending: int = 1
                    ) -> GetResponseType:
        """
        Get the list of phone book entries.

        :param page: Page number (default is 1).
        :param key_word: Keyword to search for (default is '').
        :param group_id: Group ID (default is 0).
        :param read_count: Number of entries to read (default is 50).
        :param save_type: Save type (default is 0).
        :param sort_type: Sort type (default is 1).
        :param ascending: Sort order (default is 1).
        :return: List of phone book entries.

        Usage example:
        >>> pb = Pb(session)
        >>> pb_list = pb.get_pb_list(page=1, key_word="John")
        >>> print(pb_list)
        """
        return self._session.post_get('pb/pb-list', OrderedDict((
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
        Get the count of phone book entries.

        Endpoint found by reverse engineering B310s-22 firmware, unknown usage.

        :return: Count of phone book entries.

        Usage example:
        >>> pb = Pb(session)
        >>> count = pb.pb_count()
        >>> print(count)
        """
        return self._session.post_get('pb/pb-count')

    def group_count(self) -> GetResponseType:
        """
        Get the count of phone book groups.

        Endpoint found by reverse engineering B310s-22 firmware, unknown usage.

        :return: Count of phone book groups.

        Usage example:
        >>> pb = Pb(session)
        >>> count = pb.group_count()
        >>> print(count)
        """
        return self._session.post_get('pb/group-count')

    def pb_new(self,
               group_id: int = 0,
               save_type: int = 0,
               name: str = '',
               mobile_phone: str = '',
               home_phone: str = '',
               work_phone: str = '',
               work_email: str = '') -> SetResponseType:
        """
        Add new entry to global PhoneBook

        :param group_id: Group ID (default is 0).
        :param save_type: Save type (default is 0).
        :param name: Name of the contact.
        :param mobile_phone: Mobile phone number.
        :param home_phone: Home phone number.
        :param work_phone: Work phone number.
        :param work_email: Work email address.
        :return: Set response type.

        Usage example:
        >>> pb = Pb(session)
        >>> response = pb.pb_new(name="John Doe", mobile_phone="123456789")
        >>> print(response)
        """

        class Node:
            def __init__(self, _name: str):
                self._name = _name

            def __str__(self) -> str:
                return self._name

        data = OrderedDict([
            ('GroupID', group_id),
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

        return self._session.post_set('pb/pb-new', data)

    def pb_delete(self, pb_index: int) -> SetResponseType:
        """
        Delete single PB Item by its ID

        :param pb_index: Id of PB Item you wish to delete.
        :return: Set response type.

        Usage example:
        >>> pb = Pb(session)
        >>> response = pb.pb_delete(pb_index=1)
        >>> print(response)
        """
        return self._session.post_set('pb/pb-delete', {'Index': pb_index})

    def group_delete(self, group_id: int) -> SetResponseType:
        """
        Delete Phonebook group by its ID

        :param group_id: Id of Group you wish to delete.
        :return: Set response type.

        Usage example:
        >>> pb = Pb(session)
        >>> response = pb.group_delete(group_id=1)
        >>> print(response)
        """
        return self._session.post_set('pb/group-delete', {'GroupID': group_id})

    def group_list(self,
                   page: int = 1,
                   read_count: int = 50,
                   sort_type: int = 1,
                   ascending: int = 1
                   ) -> GetResponseType:
        """
        Get the list of phone book groups.

        :param page: Page number (default is 1).
        :param read_count: Number of entries to read (default is 50).
        :param sort_type: Sort type (default is 1).
        :param ascending: Sort order (default is 1).
        :return: List of phone book groups.

        Usage example:
        >>> pb = Pb(session)
        >>> group_list = pb.group_list(page=1)
        >>> print(group_list)
        """
        return self._session.post_get('pb/group-list', OrderedDict((
            ('PageIndex', page),
            ('ReadCount', read_count),
            ('SortType', sort_type),
            ('Ascending', ascending)
        )))

    def group_new(self, name_str: str) -> SetResponseType:
        """
        Create new Phonebook group by its name

        :param name_str: Name of PB Group you wish to create.
        :return: Set response type.

        Usage example:
        >>> pb = Pb(session)
        >>> response = pb.group_new(name_str="Friends")
        >>> print(response)
        """
        return self._session.post_set('pb/group-new', {'GroupName': name_str})

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
