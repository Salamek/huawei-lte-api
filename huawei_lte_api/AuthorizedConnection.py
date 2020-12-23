import datetime
import warnings
from typing import Optional, Tuple, Union
from urllib.parse import urlparse, urlunparse
from huawei_lte_api.Connection import Connection


class AuthorizedConnection(Connection):
    LOGOUT_TIMEOUT = 300  # seconds
    login_time = None
    logged_in = False

    def __init__(self, url: str, username: Optional[str]=None, password: Optional[str]=None,
                 login_on_demand: bool=False, timeout: Union[float, Tuple[float, float], None] = None):
        # Auth info embedded in the URL may reportedly cause problems, strip it
        parsed_url = urlparse(url)
        clear_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc.rpartition("@")[-1],
            *parsed_url[2:]
        ))
        super().__init__(clear_url, timeout=timeout)
        username = username if username else parsed_url.username
        password = password if password else parsed_url.password

        from huawei_lte_api.api.User import User  # pylint: disable=cyclic-import,import-outside-toplevel
        self.user = User(self, username, password)

        if login_on_demand:
            warnings.warn(
                "login_on_demand is deprecated, and has no effect, please remove this parameter from your code! if  will get removed in next minor release.",
                DeprecationWarning
            )

        if self.user.login(True):
            self.login_time = datetime.datetime.utcnow()
            self.logged_in = True

    def _is_login_timeout(self) -> bool:
        if self.login_time is None:
            return True
        logout_time = self.login_time + datetime.timedelta(seconds=self.LOGOUT_TIMEOUT)
        return logout_time < datetime.datetime.utcnow()

    def enforce_authorized_connection(self) -> bool:
        # Check if connection timeouted or not
        if not self.logged_in or self._is_login_timeout():
            # Connection timeouted, relogin
            if self.user.login():
                self.login_time = datetime.datetime.utcnow()
                self.logged_in = True
            else:
                self.login_time = None
                self.logged_in = False

        return self.logged_in
