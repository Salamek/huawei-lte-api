import pytest
from requests.exceptions import ConnectionError as RequestsConnectionError

from huawei_lte_api.Connection import Connection


def test_connection_wrong_url() -> None:
    with pytest.raises(RequestsConnectionError):
        Connection("http://localhost")
