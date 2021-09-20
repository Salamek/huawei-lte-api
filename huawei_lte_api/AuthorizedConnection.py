import warnings

from huawei_lte_api.Connection import Connection


class AuthorizedConnection(Connection):
    def __init__(self, *args, **kwargs):
        warnings.warn("AuthorizedConnection is deprecated, use Connection instead", DeprecationWarning)
        super().__init__(*args, **kwargs)
