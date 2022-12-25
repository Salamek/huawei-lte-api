import datetime
from typing import Optional, Tuple, Iterator, TypeVar, Iterable

from binascii import hexlify
import math
import base64
from Cryptodome.Cipher import PKCS1_v1_5, PKCS1_OAEP
from Cryptodome.PublicKey.RSA import construct


T = TypeVar('T')


class Tools:
    datetime_format = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def enforce_list_response(data: dict, singular_key_name: str, plural_key_name: Optional[str] = None) -> dict:
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
    def rsa_encrypt(rsa_e: str, rsa_n: str, data: bytes, rsa_padding: int = 0) -> bytes:
        b64data = base64.b64encode(data)
        pubkey = construct((int(rsa_n, 16), int(rsa_e, 16)))

        cipher_module = {
            0: PKCS1_v1_5,
            1: PKCS1_OAEP
        }.get(rsa_padding)

        num = {
            0: 245,
            1: 214
        }.get(rsa_padding)

        if not cipher_module or not num:
            raise Exception('Unknown rsa_padding value {}'.format(rsa_padding))

        cipher = cipher_module.new(pubkey)

        blocks = int(math.ceil(len(b64data) / float(num)))
        result_chunks = []
        for i in range(blocks):
            block = b64data[i * num:(i + 1) * num]
            result_chunks.append(cipher.encrypt(block))
        result = hexlify(b''.join(result_chunks))
        if (len(result) & 1) == 0:
            return result

        return b'0' + result

    @staticmethod
    def strip_dict(filtered_dict: dict, wanted_keys: Tuple[str, ...]) -> dict:
        """
        Strips unwanted items from dict and keeps only wanted_keys
        :param filtered_dict: Dict to filter
        :param wanted_keys: Keys to keep
        :return:
        """
        return {i: filtered_dict[i] for i in filtered_dict if i in set(wanted_keys)}

    @staticmethod
    def filter_iter(data: Iterable[T], filter_options: dict) -> Iterator[T]:
        for data_item in data:
            for attr, value in filter_options.items():
                if isinstance(data_item, dict):
                    if data_item.get(attr) != value:
                        break
                else:
                    if getattr(data_item, attr) != value:
                        break
            else:
                yield data_item

    @staticmethod
    def string_to_datetime(datetime_string: str) -> datetime.datetime:
        """
        Parses datetime in format 2022-12-22 18:01:09
        :param datetime_string: string to parse
        :return: datetime.datetime
        """
        return datetime.datetime.strptime(datetime_string, Tools.datetime_format)

    @staticmethod
    def datetime_to_string(date_time: datetime.datetime) -> str:
        return date_time.strftime(Tools.datetime_format)
