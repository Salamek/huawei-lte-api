import warnings
from typing import Optional, Tuple, Union
from huawei_lte_api.Connection import Connection
from huawei_lte_api.api.User import UserSession
from urllib.parse import urlparse


class AuthorizedConnection(Connection):
    def __init__(self, *args, **kwargs):
        warnings.warn("AuthorizedConnection is deprecated, use Connection instead", DeprecationWarning)
        super().__init__(*args, **kwargs)







