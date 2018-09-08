import base64
import hashlib
from huawei_lte_api.enums.user import PasswordTypeEnum, LoginStateEnum, LoginErrorEnum
from huawei_lte_api.enums.client import ResponseEnum
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.exceptions import ResponseErrorException, \
    LoginErrorAlreadyLoginException, \
    LoginErrorUsernamePasswordModifyException, \
    LoginErrorUsernamePasswordOverrunException, \
    LoginErrorUsernamePasswordWrongException, \
    LoginErrorUsernameWrongException, \
    LoginErrorPasswordWrongException


class User(ApiGroup):
    _username = 'admin'
    _password = None

    def __init__(self, connection, username: str=None, password: str=None):
        super(User, self).__init__(connection)
        self._username = username if username else 'admin'
        self._password = password

    def state_login(self) -> dict:
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
            result = self._connection.post('user/login', {
                'Username': self._username,
                'Password': password.decode('UTF-8'),
                'password_type': password_type.value
            }, refresh_csfr=True)
        except ResponseErrorException as e:
            error_code_to_message = {
                LoginErrorEnum.USERNAME_WRONG: 'Username wrong',
                LoginErrorEnum.PASSWORD_WRONG: 'Password wrong',
                LoginErrorEnum.ALREADY_LOGIN: 'Already login',
                LoginErrorEnum.USERNAME_PWD_WRONG: 'Username and Password wrong',
                LoginErrorEnum.USERNAME_PWD_ORERRUN: 'Password overrun',
                LoginErrorEnum.USERNAME_PWD_MODIFY: 'Password modify',
            }

            error_code_to_exception = {
                LoginErrorEnum.USERNAME_WRONG: LoginErrorUsernameWrongException,
                LoginErrorEnum.PASSWORD_WRONG: LoginErrorPasswordWrongException,
                LoginErrorEnum.ALREADY_LOGIN: LoginErrorAlreadyLoginException,
                LoginErrorEnum.USERNAME_PWD_WRONG: LoginErrorUsernamePasswordWrongException,
                LoginErrorEnum.USERNAME_PWD_ORERRUN: LoginErrorUsernamePasswordOverrunException,
                LoginErrorEnum.USERNAME_PWD_MODIFY: LoginErrorUsernamePasswordModifyException,
            }

            message = error_code_to_message.get(e.code, 'Unknown')
            raise error_code_to_exception.get(e.code, ResponseErrorException)(
                '{}: {}'.format(e.code, message), e.code)

        return result == ResponseEnum.OK.value

    def login(self, force_new_login: bool=False) -> bool:
        state_login = self.state_login()
        if LoginStateEnum(int(state_login['State'])) == LoginStateEnum.LOGGED_IN and not force_new_login:
            return True

        return self._login(PasswordTypeEnum(int(state_login['password_type'])))

    def logout(self):
        return self._connection.post('user/logout', {
            'Logout': 1
        })

    def remind(self) -> dict:
        return self._connection.get('user/remind')

    def password(self) -> dict:
        return self._connection.get('user/password')

    def pwd(self) -> dict:
        return self._connection.get('user/pwd')

    def set_remind(self, remind_state):
        return self._connection.post('user/remind', {
            'remindstate': remind_state
        })
