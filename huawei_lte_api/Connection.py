from __future__ import annotations

import logging
import warnings
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from huawei_lte_api.api.User import DEFAULT_USERNAME, UserSession
from huawei_lte_api.Session import Session

if TYPE_CHECKING:
    from types import TracebackType

    import requests

_LOGGER = logging.getLogger(__name__)


class Connection(Session):
    user_session: UserSession | None

    def __init__(
        self,
        url: str,
        username: str | None = None,
        password: str | None = None,
        login_on_demand: bool = False,
        timeout: float | tuple[float, float] | None = None,
        requests_session: requests.Session | None = None,
    ) -> None:
        """
        :param requests_session: requests Session to use; if not None, closing it is the caller's responsibility
        """
        parsed_url = urlparse(url)

        # User login code
        username = username or parsed_url.username
        password = password if password else parsed_url.password

        _LOGGER.debug("Initializing Connection with URL: %s", url)
        _LOGGER.debug("Username: %s", username)
        _LOGGER.debug("Password: %s", password)

        super().__init__(url, timeout=timeout, requests_session=requests_session)
        if username or password:
            self.user_session = UserSession(
                self,
                username or DEFAULT_USERNAME,
                password,
            )
        else:
            self.user_session = None

        if login_on_demand:
            warnings.warn(
                "login_on_demand is deprecated, and has no effect, please remove this parameter from your code! if  will get removed in next minor release.",
                DeprecationWarning,
                stacklevel=2,
            )

    def close(self) -> None:
        if self.user_session:
            try:
                self.user_session.close()
            except:
                super().close()
                raise
        super().close()

    def __enter__(self) -> Connection:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> None:
        self.close()
