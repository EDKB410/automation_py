import hashlib
import random
import socket
import string

import pytest


class Utils:

    @staticmethod
    # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    def get_ip() -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def skipped(el: tuple, lst: list) -> tuple:
        if any(map(lambda x: x in el, lst)):
            return pytest.param(el, marks=pytest.mark.skip)
        return el

    def xfailed(el: tuple, lst: list) -> tuple:
        if any(map(lambda x: x in el, lst)):
            return pytest.param(el, marks=pytest.mark.xfail)
        return el

    def random_letters(size):
        return ''.join(random.choice(string.ascii_letters) for _ in range(size))

    def random_digits(size):
        return ''.join(random.choice(string.digits) for _ in range(size))

    def random_symbols(size):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

    # https://www.generacodice.com/en/articolo/2217802/OpenCart-Customer-Password-Encryption
    def encrypt_oc_password(password):
        salt = Utils.random_symbols(9)
        round_0 = hashlib.sha1(password.encode('utf-8')).hexdigest()
        round_1 = hashlib.sha1((salt + round_0).encode('utf-8')).hexdigest()
        round_2 = hashlib.sha1((salt + round_1).encode('utf-8')).hexdigest()
        return (salt, round_2)
