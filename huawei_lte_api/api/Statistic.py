from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Statistic(ApiGroup):
    def feature_roam_statistic(self) -> GetResponseType:
        return self._session.get('statistic/feature-roam-statistic')
