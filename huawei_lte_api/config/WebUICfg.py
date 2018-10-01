from huawei_lte_api.ApiGroup import ApiGroup


class WebUICfg(ApiGroup):
    def config(self):
        return self._connection.get('webuicfg/config.xml', prefix='config')
