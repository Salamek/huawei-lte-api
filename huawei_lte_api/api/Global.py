
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Global(ApiGroup):
    def module_switch(self) -> GetResponseType:
        return self._connection.get('global/module-switch')

    def storage_get_item(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('global/storage-getitem')
