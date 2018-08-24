import dicttoxml
import xmltodict
import requests
import urllib.parse
import re
from huawei_lte_api.enums.client import ResponseCodeEnum
from huawei_lte_api.exceptions import \
    ResponseErrorException, \
    ResponseErrorLoginRequiredException, \
    ResponseErrorNotSupportedException, \
    ResponseErrorSystemBusyException, \
    ResponseErrorLoginCsfrException


class Connection(object):
    csfr_re = re.compile('name="csrf_token"\s+content="(\S+)"')
    cookie_jar = None
    request_verification_tokens = []

    def __init__(self, url: str):
        if not url.endswith('/'):
            raise Exception('URL must end with /')
        self.url = url
        self._initialize_csfr_tokens_and_session()

    def reload(self):
        self._initialize_csfr_tokens_and_session()

    @staticmethod
    def _create_request_xml(data: dict, dicttoxml_xargs: dict=None) -> str:
        if not dicttoxml_xargs:
            dicttoxml_xargs = {}
        return dicttoxml.dicttoxml(data, custom_root='request', **dicttoxml_xargs)

    @staticmethod
    def _process_response_xml(xml: str) -> dict:
        return xmltodict.parse(xml, dict_constructor=dict)

    @staticmethod
    def _check_response_status(data: dict):
        error_code_to_message = {
            ResponseCodeEnum.ERROR_SYSTEM_BUSY: 'System busy',
            ResponseCodeEnum.ERROR_SYSTEM_NO_RIGHTS: 'No rights (needs login)',
            ResponseCodeEnum.ERROR_SYSTEM_NO_SUPPORT: 'No support',
            ResponseCodeEnum.ERROR_SYSTEM_UNKNOWN: 'Unknown',
            ResponseCodeEnum.ERROR_SYSTEM_CSFR: 'Session error'
        }

        error_code_to_exception = {
            ResponseCodeEnum.ERROR_SYSTEM_BUSY: ResponseErrorSystemBusyException,
            ResponseCodeEnum.ERROR_SYSTEM_NO_RIGHTS: ResponseErrorLoginRequiredException,
            ResponseCodeEnum.ERROR_SYSTEM_NO_SUPPORT: ResponseErrorNotSupportedException,
            ResponseCodeEnum.ERROR_SYSTEM_UNKNOWN:  ResponseErrorException,
            ResponseCodeEnum.ERROR_SYSTEM_CSFR: ResponseErrorLoginCsfrException
        }
        if 'error' in data:
            error_code = int(data['error']['code'])
            if not data['error']['message']:
                message = error_code_to_message.get(error_code, 'Unknown')
            else:
                message = data['error']['message']
            raise error_code_to_exception.get(error_code, ResponseErrorException)('{}: {}'.format(error_code, message), error_code)

        return data['response'] if 'response' in data else data

    def _initialize_csfr_tokens_and_session(self):
        # Reset
        self.request_verification_tokens = []

        response = requests.get(self.url)
        self.cookie_jar = response.cookies

        csfr_tokens = self.csfr_re.findall(response.content.decode('UTF-8'))
        if len(csfr_tokens):
            self.request_verification_tokens = csfr_tokens
        else:
            self.request_verification_tokens.append(self._get_token())

    def _build_final_url(self, endpoint: str, prefix: str='api') -> str:
        return urllib.parse.urljoin(self.url + '{}/'.format(prefix), endpoint)

    def post(self,
             endpoint: str,
             data: dict=None,
             refresh_csfr: bool=False,
             prefix: str='api',
             dicttoxml_xargs: dict=None
             ) -> dict:

        headers = {
            'Content-Type': 'application/xml'
        }
        if len(self.request_verification_tokens) > 1:
            headers['__RequestVerificationToken'] = self.request_verification_tokens.pop(0)
        else:
            headers['__RequestVerificationToken'] = self.request_verification_tokens[0]

        response = requests.post(
            self._build_final_url(endpoint, prefix),
            self._create_request_xml(data, dicttoxml_xargs) if data else '',
            headers=headers,
            cookies=self.cookie_jar
        )
        response.raise_for_status()

        if response.cookies:
            self.cookie_jar = response.cookies

        data = self._check_response_status(self._process_response_xml(response.content))

        if refresh_csfr:
            self.request_verification_tokens = []

        if '__RequestVerificationTokenone' in response.headers:
            self.request_verification_tokens.append(response.headers['__RequestVerificationTokenone'])
            if '__RequestVerificationTokentwo' in response.headers:
                self.request_verification_tokens.append(response.headers['__RequestVerificationTokentwo'])
        elif '__RequestVerificationToken' in response.headers:
            self.request_verification_tokens.append(response.headers['__RequestVerificationToken'])
        else:
            raise ResponseErrorException('Failed to get CSFR from POST response headers')

        return data

    def get(self, endpoint: str, params: dict=None, prefix: str='api') -> dict:
        headers = {}
        if len(self.request_verification_tokens) == 1:
            headers['__RequestVerificationToken'] = self.request_verification_tokens[0]

        response = requests.get(
            self._build_final_url(endpoint, prefix),
            params,
            headers=headers,
            cookies=self.cookie_jar
        )

        return self._check_response_status(self._process_response_xml(response.content))

    def _get_token(self):
        data = self.get('webserver/token')
        return data['token']
