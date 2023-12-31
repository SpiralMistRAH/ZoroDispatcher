import os
from eth_typing import HexStr
from eth_utils import remove_0x_prefix
from dotenv import load_dotenv
load_dotenv()
private_key = os.getenv('PRIVATE_KEY')

class EnvPrivateKey:
    def __init__(self, env: str):
        env = os.getenv(env, None)
        if env is None:
            raise LookupError(f"Can't build key from {env}")
        self._key = bytes.fromhex(remove_0x_prefix(HexStr(env)))

    @property
    def key(self) -> bytes:
        return self._key