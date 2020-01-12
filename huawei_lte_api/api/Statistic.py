from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Statistic(ApiGroup):
    def feature_roam_statistic(self) -> GetResponseType:
        return self._connection.get('statistic/feature-roam-statistic')
