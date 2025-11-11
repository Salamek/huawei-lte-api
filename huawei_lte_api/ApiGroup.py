from huawei_lte_api.Session import Session


class ApiGroup:

    def __init__(self, session: Session) -> None:
        self._session = session
