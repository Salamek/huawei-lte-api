from huawei_lte_api.ApiGroup import ApiGroup, GetResponseType


class Statistic(ApiGroup):
    def feature_roam_statistic(self) -> GetResponseType:
        return self._connection.get('statistic/feature-roam-statistic')
