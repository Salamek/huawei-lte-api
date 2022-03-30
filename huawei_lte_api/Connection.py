import warnings
from types import TracebackType
from typing import Optional, Tuple, Union, Type
from urllib.parse import urlparse

import requests

from huawei_lte_api.Session import Session
from huawei_lte_api.api.User import UserSession


class Connection(Session):
    def __init__(self,
                 url: str,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 login_on_demand: bool = False,
                 timeout: Union[float, Tuple[float, float], None] = None,
                 requests_session: Optional[requests.Session] = None
                 ):
        """
        :param requests_session: requests Session to use, closing it is the caller's responsibility
        """
        parsed_url = urlparse(url)

        # User login code
        username = username if username else parsed_url.username
        password = password if password else parsed_url.password

        super().__init__(url, timeout=timeout, requests_session=requests_session)
        self.user_session = UserSession(self, username, password) if username else None

        if login_on_demand:
            warnings.warn(
                "login_on_demand is deprecated, and has no effect, please remove this parameter from your code! if  will get removed in next minor release.",
                DeprecationWarning
            )

    def close(self) -> None:
        if self.user_session:
            try:
                self.user_session.close()
            except:
                super().close()
                raise
        super().close()

    def __enter__(self) -> 'Connection':
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self.close()
