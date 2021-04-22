import warnings
from typing import Optional, Tuple, Union
from huawei_lte_api.Connection import Connection
from urllib.parse import urlparse


class AuthorizedConnection(Connection):
    def __init__(self,
                 url: str,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 login_on_demand: bool = False,
                 timeout: Union[float, Tuple[float, float], None] = None
                 ):
        parsed_url = urlparse(url)

        # User login code
        username = username if username else parsed_url.username
        password = password if password else parsed_url.password

        from huawei_lte_api.api.User import User  # pylint: disable=cyclic-import,import-outside-toplevel
        super().__init__(url, timeout=timeout)
        self.user = User(self)
        self.user.login(username, password, True)

        if login_on_demand:
            warnings.warn(
                "login_on_demand is deprecated, and has no effect, please remove this parameter from your code! if  will get removed in next minor release.",
                DeprecationWarning
            )

    def close(self):
        self.user.logout()
        super(AuthorizedConnection, self).close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()





