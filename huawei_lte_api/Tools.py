from typing import Union

from binascii import hexlify
import math
import base64
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey.RSA import construct


class Tools:

    @staticmethod
    def enforce_list_response(data: dict, singular_key_name: str, plural_key_name: Union[str, None] = None) -> dict:
        """
        Make sure Hosts->Host is a list
        It may be returned as a single dict if only one is associated,
        as well as sometimes None.
        :return:
        """
        if not plural_key_name:
            plural_key_name = '{}s'.format(singular_key_name)
        if data.get(plural_key_name) is None:
            data[plural_key_name] = {}
        single_item = data[plural_key_name].setdefault(singular_key_name, [])
        if isinstance(single_item, dict):
            data[plural_key_name][singular_key_name] = [single_item]

        return data

    @staticmethod
    def rsa_encrypt(rsa_e: str, rsa_n: str, data: bytes) -> bytes:
        modulus = int(rsa_n, 16)
        exponent = int(rsa_e, 16)
        b64data = base64.b64encode(data)
        pubkey = construct((modulus, exponent))
        cipher = PKCS1_v1_5.new(pubkey)
        blocks = int(math.ceil(len(b64data) / 245.0))
        result_chunks = []
        for i in range(blocks):
            block = b64data[i * 245:(i + 1) * 245]
            d = cipher.encrypt(block)
            result_chunks.append(d)
        result = hexlify(b''.join(result_chunks))
        if (len(result) & 1) == 0:
            return result

        return b'0' + result
