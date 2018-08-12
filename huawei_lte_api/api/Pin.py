
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Pin(ApiGroup):
    def status(self):
        return self.connection.get('pin/status')

    def test(self):
        return self.connection.get('global/languagelist.xml', prefix='config')