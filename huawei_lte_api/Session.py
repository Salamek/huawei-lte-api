import json
import logging
import re
import urllib.parse
from types import TracebackType
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union, Type, cast
from urllib.parse import urlparse, urlunparse

import requests
import xmltodict

from huawei_lte_api.enums.client import ResponseCodeEnum
from huawei_lte_api.exceptions import \
    ResponseErrorException, \
    ResponseErrorLoginRequiredException, \
    ResponseErrorNotSupportedException, \
    ResponseErrorSystemBusyException, \
    ResponseErrorLoginCsrfException, \
    ResponseErrorWrongSessionToken, \
    RequestFormatException
from huawei_lte_api.Tools import Tools

_LOGGER = logging.getLogger(__name__)

T = TypeVar("T")
GetResponseType = Dict[str, Any]
SetResponseType = str


def _try_or_reload_and_retry(fn: Callable[..., T]) -> Callable[..., T]:
    def wrapped(*args: Any, **kw: Any) -> T:
        try:
            return fn(*args, **kw)
        except ResponseErrorLoginCsrfException:
            args[0].reload()
            return fn(*args, **kw)

    return wrapped


class Session:
    encryption_key = None
    csrf_re = re.compile(r'name="csrf_token"\s+content="(\S+)"')
    request_verification_tokens = []  # type: List[str]

    def __init__(self,
                 url: str,
                 timeout: Union[float, Tuple[float, float], None] = None,
                 requests_session: Optional[requests.Session] = None
                 ):

        # Auth info embedded in the URL may reportedly cause problems, strip it
        parsed_url = urlparse(url)
        clear_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc.rpartition("@")[-1],
            *parsed_url[2:]
        ))

        if requests_session:
            self.requests_session = requests_session
            self._custom_requests_session = True
        else:
            self.requests_session = requests.Session()
            self._custom_requests_session = False

        if not clear_url.endswith('/'):
            clear_url += '/'
        self.url = clear_url
        self.timeout = timeout

        # Try catch to close session correctly when _initialize_csrf_tokens_and_session fails
        try:
            self._initialize_csrf_tokens_and_session()
        except Exception:
            if not self._custom_requests_session:
                self.requests_session.close()
            raise

    def reload(self) -> None:
        self._initialize_csrf_tokens_and_session()

    @staticmethod
    def _create_request_xml(data: Union[dict, list, int]) -> bytes:
        wrapped_in_request = {
            'request': data
        }

        return xmltodict.unparse(wrapped_in_request).encode('utf-8')

    @staticmethod
    def _process_response_data(response: requests.Response) -> dict:
        data = response.content

        # Some endpoints respond with JSON, some XML, but the Content-Type is always
        # text/html, so we resort to content sniffing.
        if data and data.startswith(b'{'):
            return json.loads(data)

        # In some cases unsupported methods, e.g. in config namespace,
        # respond with a redirect to the home page, which may not
        # parse as XML (even though it's labeled XHTML). Try to detect
        # such cases, and return a generated "not supported" error
        # instead of letting the XML parse error pass through.
        try:
            return xmltodict.parse(data, dict_constructor=dict) if data else {}
        except:
            if response.history:
                return dict(error=dict(code=ResponseCodeEnum.ERROR_SYSTEM_NO_SUPPORT, message=''))
            raise

    @staticmethod
    def _check_response_status(data: dict) -> Union[dict, str]:
        error_code_to_message = {
            ResponseCodeEnum.ERROR_SYSTEM_BUSY.value: 'System busy',
            ResponseCodeEnum.ERROR_SYSTEM_NO_RIGHTS.value: 'No rights (needs login)',
            ResponseCodeEnum.ERROR_SYSTEM_NO_SUPPORT.value: 'No support',
            ResponseCodeEnum.ERROR_SYSTEM_UNKNOWN.value: 'Unknown',
            ResponseCodeEnum.ERROR_SYSTEM_CSRF.value: 'Session error',
            ResponseCodeEnum.ERROR_WRONG_SESSION_TOKEN.value: 'Wrong Session Token',
            ResponseCodeEnum.ERROR_FORMAT_ERROR.value: 'Request format error',
        }

        error_code_to_exception = {
            ResponseCodeEnum.ERROR_SYSTEM_BUSY.value: ResponseErrorSystemBusyException,
            ResponseCodeEnum.ERROR_SYSTEM_NO_RIGHTS.value: ResponseErrorLoginRequiredException,
            ResponseCodeEnum.ERROR_SYSTEM_NO_SUPPORT.value: ResponseErrorNotSupportedException,
            ResponseCodeEnum.ERROR_SYSTEM_UNKNOWN.value: ResponseErrorException,
            ResponseCodeEnum.ERROR_SYSTEM_CSRF.value: ResponseErrorLoginCsrfException,
            ResponseCodeEnum.ERROR_WRONG_SESSION_TOKEN.value: ResponseErrorWrongSessionToken,
            ResponseCodeEnum.ERROR_FORMAT_ERROR.value: RequestFormatException,
        }
        if 'error' in data:
            error_code = int(data['error']['code'])
            if not data['error']['message']:
                message = error_code_to_message.get(error_code, 'Unknown')
            else:
                message = data['error']['message']
            raise error_code_to_exception.get(error_code, ResponseErrorException)(
                '{}: {}'.format(error_code, message),
                error_code
            )

        response = data['response'] if 'response' in data else data
        return response if response is not None else {}

    def _initialize_csrf_tokens_and_session(self) -> None:
        # Reset
        self.request_verification_tokens = []

        # Lets try to parse csrf_token from homepage html head meta[name="csrf_token"]
        response = self.requests_session.get(self.url, timeout=self.timeout)

        csrf_tokens = self.csrf_re.findall(response.content.decode('UTF-8'))
        if csrf_tokens:
            self.request_verification_tokens = csrf_tokens
        else:
            # If we did not find anything in HTML, lets try to ask API for it
            token = self._get_token()
            if token is not None:
                self.request_verification_tokens.append(token)

    def _build_final_url(self, endpoint: str, prefix: str = 'api') -> str:
        return urllib.parse.urljoin(self.url + '{}/'.format(prefix), endpoint)

    def _encrypt_data(self, data: bytes) -> bytes:
        rsa_padding = self._get_rsa_padding()
        pubkey_data = self._get_encryption_key()
        rsa_e = pubkey_data.get('encpubkeye')
        rsa_n = pubkey_data.get('encpubkeyn')
        if not rsa_n or not rsa_e:
            raise Exception('No pub key was found')
        return Tools.rsa_encrypt(rsa_e, rsa_n, data, rsa_padding)

    def post_get(self,
                 endpoint: str,
                 data: Union[dict, list, int, None] = None,
                 refresh_csrf: bool = False,
                 prefix: str = 'api',
                 is_encrypted: bool = False) \
            -> GetResponseType:
        return cast(
            GetResponseType,
            self._post(endpoint, data, refresh_csrf, prefix, is_encrypted)
        )

    def post_set(self,
                 endpoint: str,
                 data: Union[dict, list, int, None] = None,
                 refresh_csrf: bool = False,
                 prefix: str = 'api',
                 is_encrypted: bool = False) \
            -> SetResponseType:
        return cast(
            SetResponseType,
            self._post(endpoint, data, refresh_csrf, prefix, is_encrypted)
        )

    @_try_or_reload_and_retry
    def _post(self,
              endpoint: str,
              data: Union[dict, list, int, None] = None,
              refresh_csrf: bool = False,
              prefix: str = 'api',
              is_encrypted: bool = False) \
            -> Union[GetResponseType, SetResponseType]:

        headers = {}

        if is_encrypted:
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8;enc'
            headers['encrypt_transmit'] = 'encrypt_transmit'
        else:
            headers['Content-Type'] = 'application/xml'

        if self.request_verification_tokens:
            if len(self.request_verification_tokens) > 1:
                headers['__RequestVerificationToken'] = self.request_verification_tokens.pop(0)
            else:
                headers['__RequestVerificationToken'] = self.request_verification_tokens[0]

        data_encoded = self._create_request_xml(data) if data else b''
        response = self.requests_session.post(
            self._build_final_url(endpoint, prefix),
            data=self._encrypt_data(data_encoded) if is_encrypted else data_encoded,
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()

        response_data = cast(str, self._check_response_status(self._process_response_data(response)))

        if refresh_csrf:
            self.request_verification_tokens = []

        if '__RequestVerificationTokenone' in response.headers:
            self.request_verification_tokens.append(response.headers['__RequestVerificationTokenone'])
            if '__RequestVerificationTokentwo' in response.headers:
                self.request_verification_tokens.append(response.headers['__RequestVerificationTokentwo'])
        elif '__RequestVerificationToken' in response.headers:
            self.request_verification_tokens.append(response.headers['__RequestVerificationToken'])
        else:
            _LOGGER.debug('Failed to get CSRF from POST response headers')

        return response_data

    def post_file(self,
                  endpoint: str,
                  files: dict,
                  data: Optional[dict] = None,
                  prefix: str = 'api',
                  ) -> str:

        if self.request_verification_tokens:
            if data is None:
                data = {}
            data['csrf_token'] = self.request_verification_tokens[0]

        response = self.requests_session.post(
            self._build_final_url(endpoint, prefix),
            files=files,
            data=data,
            timeout=self.timeout
        )
        response.raise_for_status()

        return response.content.decode('UTF-8').lower()

    @_try_or_reload_and_retry
    def get(self, endpoint: str, params: Optional[dict] = None, prefix: str = 'api') -> dict:
        headers = {}
        if len(self.request_verification_tokens) == 1:
            headers['__RequestVerificationToken'] = self.request_verification_tokens[0]

        response = self.requests_session.get(
            self._build_final_url(endpoint, prefix),
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

        return cast(dict, self._check_response_status(self._process_response_data(response)))

    def _get_token(self) -> Optional[str]:
        try:
            data = self.get('webserver/token')
            return data['token']
        except ResponseErrorNotSupportedException:
            try:
                data = self.get('webserver/SesTokInfo')
                return data['TokInfo']
            except ResponseErrorNotSupportedException:
                return None

    def _get_encryption_key(self) -> dict:
        if not self.encryption_key:
            self.encryption_key = self.get('webserver/publickey')
        return self.encryption_key

    def _get_rsa_padding(self) -> int:
        state_login = self.get('user/state-login')
        return int(state_login['rsapadingtype']) if 'rsapadingtype' in state_login else 0

    def close(self) -> None:
        if not self._custom_requests_session:
            self.requests_session.close()

    def __enter__(self) -> 'Session':
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self.close()
