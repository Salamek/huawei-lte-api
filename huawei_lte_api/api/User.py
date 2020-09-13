import base64
import hashlib
import time
from typing import Optional
import requests
from huawei_lte_api.enums.user import PasswordTypeEnum, LoginStateEnum, LoginErrorEnum
from huawei_lte_api.enums.client import ResponseEnum
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import Connection, GetResponseType, SetResponseType
from huawei_lte_api.exceptions import ResponseErrorException, \
    LoginErrorAlreadyLoginException, \
    LoginErrorUsernamePasswordModifyException, \
    LoginErrorUsernamePasswordOverrunException, \
    LoginErrorUsernamePasswordWrongException, \
    LoginErrorUsernameWrongException, \
    LoginErrorPasswordWrongException, \
    ResponseErrorNotSupportedException


class User(ApiGroup):
    _username = 'admin'
    _password = None

    def __init__(self, connection: Connection, username: Optional[str]=None, password: Optional[str]=None):
        super().__init__(connection)
        self._username = username if username else 'admin'
        self._password = password

    def state_login(self) -> GetResponseType:
        return self._connection.get('user/state-login')

    def _login(self, password_type: PasswordTypeEnum=PasswordTypeEnum.BASE_64) -> bool:
        if not self._password:
            password = b''
        else:
            if password_type == PasswordTypeEnum.SHA256:
                concentrated = b''.join([
                    self._username.encode('UTF-8'),
                    base64.b64encode(hashlib.sha256(self._password.encode('UTF-8')).hexdigest().encode('ascii')),
                    self._connection.request_verification_tokens[0].encode('UTF-8')
                ])
                password = base64.b64encode(hashlib.sha256(concentrated).hexdigest().encode('ascii'))
            else:
                password = base64.b64encode(self._password.encode('UTF-8'))

        try:
            result = self._connection.post_set('user/login', {
                'Username': self._username,
                'Password': password.decode('UTF-8'),
                'password_type': password_type.value
            }, refresh_csrf=True)
        except ResponseErrorException as e:
            error_code_to_message = {
                LoginErrorEnum.USERNAME_WRONG.value: 'Username wrong',
                LoginErrorEnum.PASSWORD_WRONG.value: 'Password wrong',
                LoginErrorEnum.ALREADY_LOGIN.value: 'Already login',
                LoginErrorEnum.USERNAME_PWD_WRONG.value: 'Username and Password wrong',
                LoginErrorEnum.USERNAME_PWD_ORERRUN.value: 'Password overrun',
                LoginErrorEnum.USERNAME_PWD_MODIFY.value: 'Password modify',
            }

            error_code_to_exception = {
                LoginErrorEnum.USERNAME_WRONG.value: LoginErrorUsernameWrongException,
                LoginErrorEnum.PASSWORD_WRONG.value: LoginErrorPasswordWrongException,
                LoginErrorEnum.ALREADY_LOGIN.value: LoginErrorAlreadyLoginException,
                LoginErrorEnum.USERNAME_PWD_WRONG.value: LoginErrorUsernamePasswordWrongException,
                LoginErrorEnum.USERNAME_PWD_ORERRUN.value: LoginErrorUsernamePasswordOverrunException,
                LoginErrorEnum.USERNAME_PWD_MODIFY.value: LoginErrorUsernamePasswordModifyException,
            }

            message = error_code_to_message.get(e.code, 'Unknown')
            raise error_code_to_exception.get(e.code, ResponseErrorException)(
                '{}: {}'.format(e.code, message), e.code)

        return result == ResponseEnum.OK.value

    def login(self, force_new_login: bool=False) -> bool:
        tries = 5
        for i in range(tries):
            try:
                state_login = self.state_login()
            except requests.exceptions.ConnectionError:
                # Some models reportedly close the connection if we attempt to access login state too soon after
                # setting up the session etc. In that case, retry a few times. The error is reported to be
                # ConnectionError: (
                #     'Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
                if i == tries - 1:
                    raise
                time.sleep((i + 1)/10)
            except ResponseErrorNotSupportedException:
                return True

        if LoginStateEnum(int(state_login['State'])) == LoginStateEnum.LOGGED_IN and not force_new_login:
            return True

        return self._login(PasswordTypeEnum(int(state_login['password_type'])))

    def logout(self) -> SetResponseType:
        return self._connection.post_set('user/logout', {
            'Logout': 1
        })

    def remind(self) -> GetResponseType:
        return self._connection.get('user/remind')

    def password(self) -> GetResponseType:
        return self._connection.get('user/password')

    def pwd(self) -> GetResponseType:
        return self._connection.get('user/pwd')

    def set_remind(self, remind_state: str) -> SetResponseType:
        return self._connection.post_set('user/remind', {
            'remindstate': remind_state
        })

    def authentication_login(self) -> GetResponseType:
        return self._connection.get('user/authentication_login')

    def challenge_login(self) -> GetResponseType:
        return self._connection.get('user/challenge_login')

    def hilink_login(self) -> GetResponseType:
        return self._connection.get('user/hilink_login')

    def history_login(self) -> GetResponseType:
        return self._connection.get('user/history-login')

    def heartbeat(self) -> GetResponseType:
        return self._connection.get('user/heartbeat')

    def web_feature_switch(self) -> GetResponseType:
        return self._connection.get('user/web-feature-switch')

    def input_event(self) -> GetResponseType:
        """
       Endpoint found by reverse engineering B310s-22 firmware, unknown usage
       :return:
       """
        return self._connection.get('user/input_event')

    def screen_state(self) -> GetResponseType:
        """
       Endpoint found by reverse engineering B310s-22 firmware, unknown usage
       :return:
       """
        return self._connection.get('user/screen_state')

    def session(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('user/session')
