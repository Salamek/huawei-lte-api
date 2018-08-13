import base64
import hashlib
from huawei_lte_api.enums.user import PasswordTypeEnum, LoginStateEnum
from huawei_lte_api.enums.client import ResponseEnum
from huawei_lte_api.ApiGroup import ApiGroup


class User(ApiGroup):
    _username = 'admin'
    _password = None

    def _state_login(self) -> dict:
        return self._connection.get('user/state-login')

    def _login(self, password_type: PasswordTypeEnum=PasswordTypeEnum.BASE_64) -> bool:
        if password_type == PasswordTypeEnum.SHA256:
            concentrated = b''.join([
                self._username.encode('UTF-8'),
                base64.b64encode(hashlib.sha256(self._password.encode('UTF-8')).hexdigest().encode('ascii')),
                self._connection.request_verification_tokens[0].encode('UTF-8')
            ])
            password = base64.b64encode(hashlib.sha256(concentrated).hexdigest().encode('ascii'))
        else:
            password = base64.b64encode(self._password.encode('UTF-8'))

        result = self._connection.post('user/login', {
            'Username': self._username,
            'Password': password.decode('UTF-8'),
            'password_type': password_type.value
        }, refresh_csfr=True)

        return result == ResponseEnum.OK.value

    def _enforce_logged(self, force_new_login: bool=False) -> bool:
        state_login = self._state_login()
        if LoginStateEnum(int(state_login['State'])) == LoginStateEnum.LOGGED_IN and not force_new_login:
            return True

        return self._login(PasswordTypeEnum(int(state_login['password_type'])))

    def login(self, username: str=None, password: str=None) -> bool:
        self._username = username
        self._password = password
        return self._enforce_logged(True)

    def logout(self):
        return self._connection.post('user/logout', {
            'Logout': 1
        })

    def remind(self):
        return self._connection.get('user/remind')

    def password(self):
        return self._connection.get('user/password')

    def set_remind(self, remind_state):
        return self._connection.post('user/remind', {
            'remindstate': remind_state
        })
