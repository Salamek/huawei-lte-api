from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Global(ApiGroup):
    def module_switch(self) -> GetResponseType:
        """
        Get the status of the module switch.

        :return: Module switch status.

        Usage example:
        >>> global_api = Global(session)
        >>> module_switch_status = global_api.module_switch()
        >>> print(module_switch_status)
        """
        return self._session.get("global/module-switch")

    def storage_get_item(self) -> GetResponseType:
        """
        Get storage item.

        Endpoint found by reverse engineering B310s-22 firmware, unknown usage.

        :return: Storage item.

        Usage example:
        >>> global_api = Global(session)
        >>> storage_item = global_api.storage_get_item()
        >>> print(storage_item)
        """
        return self._session.get("global/storage-getitem")

    def custommenu_url(self) -> GetResponseType:
        """
        Get custom menu URL.

        :return: Custom menu URL.

        Usage example:
        >>> global_api = Global(session)
        >>> custom_menu_url = global_api.custommenu_url()
        >>> print(custom_menu_url)
        """
        return self._session.get("global/custommenu-url")
