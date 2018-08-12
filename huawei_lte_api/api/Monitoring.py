
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Monitoring(ApiGroup):
    def converged_status(self):
        return self.connection.get('monitoring/converged-status')

    def status(self):
        return self.connection.get('monitoring/status')

    def check_notifications(self):
        return self.connection.get('monitoring/check-notifications')

    def traffic_statistics(self):
        return self.connection.get('monitoring/traffic-statistics')