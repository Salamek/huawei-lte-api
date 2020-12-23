import warnings
from typing import Optional, Tuple, Union
from huawei_lte_api.Connection import Connection


class AuthorizedConnection(Connection):
    def __init__(self,
                 url: str,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 login_on_demand: bool = False,
                 timeout: Union[float, Tuple[float, float], None] = None
                 ):

        if login_on_demand:
            warnings.warn(
                "login_on_demand is deprecated, and has no effect, please remove this parameter from your code! if  will get removed in next minor release.",
                DeprecationWarning
            )

        super().__init__(url, username=username, password=password, timeout=timeout)



