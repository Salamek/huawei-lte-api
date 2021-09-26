import base64
import hashlib
import time
from types import TracebackType
from typing import Union, Type, Optional
import requests

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType, Session
from huawei_lte_api.enums.client import ResponseEnum
from huawei_lte_api.enums.user import PasswordTypeEnum, LoginStateEnum, LoginErrorEnum
from huawei_lte_api.exceptions import ResponseErrorException, \
    LoginErrorAlreadyLoginException, \
    LoginErrorUsernamePasswordModifyException, \
    LoginErrorUsernamePasswordOverrunException, \
    LoginErrorUsernamePasswordWrongException, \
    LoginErrorUsernameWrongException, \
    LoginErrorPasswordWrongException, \
    ResponseErrorNotSupportedException


class UserSession:
    def __init__(self, session: Session, username: str, password: Union[str, None] = None):
        self.user = User(session)
        self.user.login(username, password, True)

    def close(self) -> None:
        self.user.logout()

    def __enter__(self) -> 'UserSession':
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self.close()


class User(ApiGroup):

    def state_login(self) -> GetResponseType:
        return self._session.get('user/state-login')

    def _login(self, username: str, password: Union[str, None], password_type: PasswordTypeEnum = PasswordTypeEnum.BASE_64) -> bool:
        if not password:
            password_encoded = b''
        else:
            if password_type == PasswordTypeEnum.SHA256:
                concentrated = b''.join([
                    username.encode('UTF-8'),
                    base64.b64encode(hashlib.sha256(password.encode('UTF-8')).hexdigest().encode('ascii')),
                    self._session.request_verification_tokens[0].encode('UTF-8')
                ])
                password_encoded = base64.b64encode(hashlib.sha256(concentrated).hexdigest().encode('ascii'))
            else:
                password_encoded = base64.b64encode(password.encode('UTF-8'))

        try:
            result = self._session.post_set('user/login', {
                'Username': username,
                'Password': password_encoded.decode('UTF-8'),
                'password_type': password_type.value
            }, refresh_csrf=True)
        except ResponseErrorException as e:
            error_code_to_message = {
                LoginErrorEnum.USERNAME_WRONG.value: 'Username wrong',
                LoginErrorEnum.PASSWORD_WRONG.value: 'Password wrong',
                LoginErrorEnum.ALREADY_LOGIN.value: 'Already login',
                LoginErrorEnum.USERNAME_PWD_WRONG.value: 'Username and Password wrong',
                LoginErrorEnum.USERNAME_PWD_OVERRUN.value: 'Password overrun',
                LoginErrorEnum.USERNAME_PWD_MODIFY.value: 'Password modify',
            }

            error_code_to_exception = {
                LoginErrorEnum.USERNAME_WRONG.value: LoginErrorUsernameWrongException,
                LoginErrorEnum.PASSWORD_WRONG.value: LoginErrorPasswordWrongException,
                LoginErrorEnum.ALREADY_LOGIN.value: LoginErrorAlreadyLoginException,
                LoginErrorEnum.USERNAME_PWD_WRONG.value: LoginErrorUsernamePasswordWrongException,
                LoginErrorEnum.USERNAME_PWD_OVERRUN.value: LoginErrorUsernamePasswordOverrunException,
                LoginErrorEnum.USERNAME_PWD_MODIFY.value: LoginErrorUsernamePasswordModifyException,
            }

            message = error_code_to_message.get(e.code, 'Unknown')
            raise error_code_to_exception.get(e.code, ResponseErrorException)(
                '{}: {}'.format(e.code, message), e.code)

        return result == ResponseEnum.OK.value

    def login(self, username: str, password: Union[str, None], force_new_login: bool = False) -> bool:
        username = username if username else 'admin'
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
                time.sleep((i + 1) / 10)
            except ResponseErrorNotSupportedException:
                return True

        if LoginStateEnum(int(state_login['State'])) == LoginStateEnum.LOGGED_IN and not force_new_login:
            return True

        return self._login(username, password, PasswordTypeEnum(int(state_login['password_type'])))

    def logout(self) -> SetResponseType:
        return self._session.post_set('user/logout', {
            'Logout': 1
        })

    def remind(self) -> GetResponseType:
        return self._session.get('user/remind')

    def password(self) -> GetResponseType:
        return self._session.get('user/password')

    def pwd(self) -> GetResponseType:
        return self._session.get('user/pwd')

    def set_remind(self, remind_state: str) -> SetResponseType:
        return self._session.post_set('user/remind', {
            'remindstate': remind_state
        })

    def authentication_login(self) -> GetResponseType:
        return self._session.get('user/authentication_login')

    def challenge_login(self) -> GetResponseType:
        return self._session.get('user/challenge_login')

    def hilink_login(self) -> GetResponseType:
        return self._session.get('user/hilink_login')

    def history_login(self) -> GetResponseType:
        return self._session.get('user/history-login')

    def heartbeat(self) -> GetResponseType:
        return self._session.get('user/heartbeat')

    def web_feature_switch(self) -> GetResponseType:
        return self._session.get('user/web-feature-switch')

    def input_event(self) -> GetResponseType:
        """
       Endpoint found by reverse engineering B310s-22 firmware, unknown usage
       :return:
       """
        return self._session.get('user/input_event')

    def screen_state(self) -> GetResponseType:
        """
       Endpoint found by reverse engineering B310s-22 firmware, unknown usage
       :return:
       """
        return self._session.get('user/screen_state')

    def session(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('user/session')
