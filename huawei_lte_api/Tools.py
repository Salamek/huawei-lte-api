from typing import Union


class Tools:

    @staticmethod
    def enforce_list_response(data: dict, singular_key_name: str, plural_key_name: Union[str, None] = None) -> dict:
        """
        Make sure Hosts->Host is a list
        It may be returned as a single dict if only one is associated,
        as well as sometimes None.
        :return:
        """
        if not plural_key_name:
            plural_key_name = '{}s'.format(singular_key_name)
        if data.get(plural_key_name) is None:
            data[plural_key_name] = {}
        single_item = data[plural_key_name].setdefault(singular_key_name, [])
        if isinstance(single_item, dict):
            data[plural_key_name][singular_key_name] = [single_item]

        return data
