import pytest
from huawei_lte_api.Connection import Connection


def test_connection_wrong_url() -> None:
    with pytest.raises(Exception):
        Connection('http://localhost')

