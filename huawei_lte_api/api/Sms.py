
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Sms(ApiGroup):
    def get_cbsnewslist(self):
        return self._connection.get('sms/get-cbsnewslist')
