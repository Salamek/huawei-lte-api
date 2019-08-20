from huawei_lte_api.ApiGroup import ApiGroup


class Statistic(ApiGroup):
    def feature_roam_statistic(self) -> dict:
        return self._connection.get('statistic/feature-roam-statistic')
