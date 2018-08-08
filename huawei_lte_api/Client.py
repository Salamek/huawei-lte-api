import dicttoxml
import xmltodict
import requests
import urllib.parse
import base64
import hashlib
import re

from huawei_lte_api.exceptions import ResponseErrorException
from huawei_lte_api.enums.user import PasswordTypeEnum, LoginStateEnum


class Client(object):
    csfr_re = re.compile('name="csrf_token"\s+content="(\S+)"')
    cookie_jar = None
    username = 'admin'
    password = None
    request_verification_tokens = []

    def __init__(self, url: str):
        if not url.endswith('/'):
            raise Exception('URL must end with /')
        self.url = url
        self._initialize_csfr_tokens_and_session()

    @staticmethod
    def _create_request_xml(data: dict) -> str:
        return dicttoxml.dicttoxml(data, custom_root='requests')

    @staticmethod
    def _process_response_xml(xml: str) -> dict:
        return xmltodict.parse(xml, dict_constructor=dict)

    @staticmethod
    def _check_response_status(data: dict):
        if 'error' in data:
            raise ResponseErrorException('{}: {}'.format(data['error']['code'], data['error']['message']))

        return data

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

    def _build_final_url(self, endpoint: str) -> str:
        return urllib.parse.urljoin(self.url + 'api/', endpoint)

    def _post(self, endpoint: str, data: dict, refresh_csfr: bool=False) -> dict:
        headers = {
            'Content-Type': 'application/xml'
        }
        if len(self.request_verification_tokens) > 1:
            headers['__RequestVerificationToken'] = self.request_verification_tokens.pop(0)
        else:
            headers['__RequestVerificationToken'] = self.request_verification_tokens[0]

        response = requests.post(
            self._build_final_url(endpoint),
            self._create_request_xml(data),
            headers=headers,
            cookies=self.cookie_jar
        )
        response.raise_for_status()

        self.cookie_jar = response.cookies

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

        return self._check_response_status(self._process_response_xml(response.content))

    def _get(self, endpoint: str, params: dict=None) -> dict:
        headers = {}
        if len(self.request_verification_tokens) > 0:
            headers['__RequestVerificationToken'] = self.request_verification_tokens[0]

        response = requests.get(
            self._build_final_url(endpoint),
            params,
            headers=headers,
            cookies=self.cookie_jar
        )
        return self._check_response_status(self._process_response_xml(response.content))

    def _state_login(self) -> dict:
        return self._get('user/state-login')['response']

    def _login(self, password_type: PasswordTypeEnum=PasswordTypeEnum.BASE_64) -> bool:
        if password_type == PasswordTypeEnum.SHA256:
            concentrated = b''.join([
                self.username.encode('UTF-8'),
                base64.b64encode(hashlib.sha256(self.password.encode('UTF-8')).hexdigest().encode('ascii')),
                self.request_verification_tokens[0].encode('UTF-8')
            ])
            password = base64.b64encode(hashlib.sha256(concentrated).hexdigest().encode('ascii'))
        else:
            password = base64.b64encode(self.password.encode('UTF-8'))

        return self._post('user/login', {
            'Username': self.username,
            'Password': password.decode('UTF-8'),
            'password_type': password_type.value
        }, refresh_csfr=False)['response'] == 'OK'

    def _get_token(self):
        data = self._get('webserver/token')
        return data['response']['token']

    def _enforce_logged(self, force_new_login: bool=False) -> bool:
        state_login = self._state_login()
        if LoginStateEnum(int(state_login['State'])) == LoginStateEnum.LOGGED_IN and not force_new_login:
            return True

        return self._login(PasswordTypeEnum(int(state_login['password_type'])))

    def login(self, username: str=None, password: str=None) -> bool:
        self.username = username
        self.password = password
        return self._enforce_logged(True)