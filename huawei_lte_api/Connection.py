import logging
import re
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union, cast
import urllib.parse
import dicttoxml
import xmltodict
import requests
from huawei_lte_api.enums.client import ResponseCodeEnum
from huawei_lte_api.exceptions import \
    ResponseErrorException, \
    ResponseErrorLoginRequiredException, \
    ResponseErrorNotSupportedException, \
    ResponseErrorSystemBusyException, \
    ResponseErrorLoginCsrfException


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


class Connection:
    csrf_re = re.compile(r'name="csrf_token"\s+content="(\S+)"')
    request_verification_tokens = []  # type: List[str]

    def __init__(self, url: str, timeout: Union[float, Tuple[float, float], None] = None):
        self.session = requests.Session()
        self.url = url
        self.timeout = timeout
        if not self.url.endswith('/'):
            self.url += '/'
        self._initialize_csrf_tokens_and_session()

    def reload(self) -> None:
        self._initialize_csrf_tokens_and_session()

    @staticmethod
    def _create_request_xml(data: Union[dict, list], dicttoxml_xargs: Optional[dict]=None) -> bytes:
        if not dicttoxml_xargs:
            dicttoxml_xargs = {}

        dicttoxml_xargs['attr_type'] = False
        return dicttoxml.dicttoxml(data, custom_root='request', **dicttoxml_xargs)

    @staticmethod
    def _process_response_xml(response: requests.Response) -> dict:
        # In some cases unsupported methods, e.g. in config namespace,
        # respond with a redirect to the home page, which may not
        # parse as XML (even though it's labeled XHTML). Try to detect
        # such cases, and return a generated "not supported" error
        # instead of letting the XML parse error pass through.
        xml = response.content
        try:
            return xmltodict.parse(xml, dict_constructor=dict) if xml else {}
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
            ResponseCodeEnum.ERROR_SYSTEM_CSRF.value: 'Session error'
        }

        error_code_to_exception = {
            ResponseCodeEnum.ERROR_SYSTEM_BUSY.value: ResponseErrorSystemBusyException,
            ResponseCodeEnum.ERROR_SYSTEM_NO_RIGHTS.value: ResponseErrorLoginRequiredException,
            ResponseCodeEnum.ERROR_SYSTEM_NO_SUPPORT.value: ResponseErrorNotSupportedException,
            ResponseCodeEnum.ERROR_SYSTEM_UNKNOWN.value:  ResponseErrorException,
            ResponseCodeEnum.ERROR_SYSTEM_CSRF.value: ResponseErrorLoginCsrfException
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
        response = self.session.get(self.url, timeout=self.timeout)

        csrf_tokens = self.csrf_re.findall(response.content.decode('UTF-8'))
        if csrf_tokens:
            self.request_verification_tokens = csrf_tokens
        else:
            # If we did not find anything in HTML, lets try to ask API for it
            token = self._get_token()
            if token is not None:
                self.request_verification_tokens.append(token)

    def _build_final_url(self, endpoint: str, prefix: str='api') -> str:
        return urllib.parse.urljoin(self.url + '{}/'.format(prefix), endpoint)

    def post_get(self,
                 endpoint: str,
                 data: Union[dict, list, None]=None,
                 refresh_csrf: bool=False,
                 prefix: str='api',
                 dicttoxml_xargs: Optional[dict]=None) \
                 -> GetResponseType:
        return cast(
            GetResponseType,
            self._post(endpoint, data, refresh_csrf, prefix, dicttoxml_xargs)
        )

    def post_set(self,
                 endpoint: str,
                 data: Union[dict, list, None]=None,
                 refresh_csrf: bool=False,
                 prefix: str='api',
                 dicttoxml_xargs: Optional[dict]=None) \
                 -> SetResponseType:
        return cast(
            SetResponseType,
            self._post(endpoint, data, refresh_csrf, prefix, dicttoxml_xargs)
        )

    @_try_or_reload_and_retry
    def _post(self,
              endpoint: str,
              data: Union[dict, list, None]=None,
              refresh_csrf: bool=False,
              prefix: str='api',
              dicttoxml_xargs: Optional[dict]=None) \
              -> Union[GetResponseType, SetResponseType]:

        headers = {
            'Content-Type': 'application/xml'
        }
        if self.request_verification_tokens:
            if len(self.request_verification_tokens) > 1:
                headers['__RequestVerificationToken'] = self.request_verification_tokens.pop(0)
            else:
                headers['__RequestVerificationToken'] = self.request_verification_tokens[0]

        response = self.session.post(
            self._build_final_url(endpoint, prefix),
            data=self._create_request_xml(data, dicttoxml_xargs) if data else b'',
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()

        response_data = cast(str, self._check_response_status(self._process_response_xml(response)))

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
                  data: Optional[dict]=None,
                  prefix: str = 'api',
                  ) -> str:

        if self.request_verification_tokens:
            if data is None:
                data = {}
            data['csrf_token'] = self.request_verification_tokens[0]

        response = self.session.post(
            self._build_final_url(endpoint, prefix),
            files=files,
            data=data,
            timeout=self.timeout
        )
        response.raise_for_status()

        return response.content.decode('UTF-8').lower()

    @_try_or_reload_and_retry
    def get(self, endpoint: str, params: Optional[dict]=None, prefix: str='api') -> dict:
        headers = {}
        if len(self.request_verification_tokens) == 1:
            headers['__RequestVerificationToken'] = self.request_verification_tokens[0]

        response = self.session.get(
            self._build_final_url(endpoint, prefix),
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

        return cast(dict, self._check_response_status(self._process_response_xml(response)))

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
