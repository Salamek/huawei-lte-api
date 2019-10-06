import logging
import re
from typing import Dict, List, Optional, Tuple, Type, Union
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

def _try_or_reload_and_retry(fn):
    def wrapped(*args, **kw):
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

    def reload(self):
        self._initialize_csrf_tokens_and_session()

    @staticmethod
    def _create_request_xml(data: dict, dicttoxml_xargs: Optional[dict]=None) -> str:
        if not dicttoxml_xargs:
            dicttoxml_xargs = {}
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
    def _check_response_status(data: dict) -> dict:
        error_code_to_message = {
            ResponseCodeEnum.ERROR_SYSTEM_BUSY: 'System busy',
            ResponseCodeEnum.ERROR_SYSTEM_NO_RIGHTS: 'No rights (needs login)',
            ResponseCodeEnum.ERROR_SYSTEM_NO_SUPPORT: 'No support',
            ResponseCodeEnum.ERROR_SYSTEM_UNKNOWN: 'Unknown',
            ResponseCodeEnum.ERROR_SYSTEM_CSRF: 'Session error'
        }  # type: Dict[int, str]

        error_code_to_exception = {
            ResponseCodeEnum.ERROR_SYSTEM_BUSY: ResponseErrorSystemBusyException,
            ResponseCodeEnum.ERROR_SYSTEM_NO_RIGHTS: ResponseErrorLoginRequiredException,
            ResponseCodeEnum.ERROR_SYSTEM_NO_SUPPORT: ResponseErrorNotSupportedException,
            ResponseCodeEnum.ERROR_SYSTEM_UNKNOWN:  ResponseErrorException,
            ResponseCodeEnum.ERROR_SYSTEM_CSRF: ResponseErrorLoginCsrfException
        }  # type: Dict[int, Type[ResponseErrorException]]
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

    def _initialize_csrf_tokens_and_session(self):
        # Reset
        self.request_verification_tokens = []

        response = self.session.get(self.url, timeout=self.timeout)

        csrf_tokens = self.csrf_re.findall(response.content.decode('UTF-8'))
        if csrf_tokens:
            self.request_verification_tokens = csrf_tokens
        else:
            token = self._get_token()
            if token is not None:
                self.request_verification_tokens.append(token)

    def _build_final_url(self, endpoint: str, prefix: str='api') -> str:
        return urllib.parse.urljoin(self.url + '{}/'.format(prefix), endpoint)

    @_try_or_reload_and_retry
    def post(self,
             endpoint: str,
             data: Optional[dict]=None,
             refresh_csrf: bool=False,
             prefix: str='api',
             dicttoxml_xargs: Optional[dict]=None
             ) -> dict:

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
            data=self._create_request_xml(data, dicttoxml_xargs) if data else '',
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()

        data = self._check_response_status(self._process_response_xml(response))

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

        return data

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

        return self._check_response_status(self._process_response_xml(response))

    def _get_token(self):
        try:
            data = self.get('webserver/token')
        except ResponseErrorNotSupportedException:
            return None
        return data['token']
