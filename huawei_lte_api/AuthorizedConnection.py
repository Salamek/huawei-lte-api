from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from huawei_lte_api.Connection import Connection

if TYPE_CHECKING:
    import requests


class AuthorizedConnection(Connection):
    def __init__(
        self,
        url: str,
        username: str | None = None,
        password: str | None = None,
        login_on_demand: bool = False,
        timeout: float | tuple[float, float] | None = None,
        requests_session: requests.Session | None = None,
    ) -> None:
        warnings.warn("AuthorizedConnection is deprecated, use Connection instead", DeprecationWarning, stacklevel=2)
        super().__init__(
            url,
            username=username,
            password=password,
            login_on_demand=login_on_demand,
            timeout=timeout,
            requests_session=requests_session,
        )
