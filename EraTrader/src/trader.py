from zksync2.module.module_builder import ZkSyncBuilder
from eth_account import Account
from eth_account.signers.local import LocalAccount
from utils import EnvPrivateKey
from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.core.types import EthBlockParams
import os
from dotenv import load_dotenv
load_dotenv()

wallets = [key for key in os.environ.keys() if key.startswith("PRIVATE_KEY")]  

# private_key = os.getenv('PRIVATE_KEY')

sdk = ZkSyncBuilder.build("https://testnet.era.zksync.dev")

print("Connected")

# Controls which network is being used
ZKSYNC_PROVIDER = "https://zksync2-testnet.zksync.dev"
# ZKSYNC_PROVIDER = "https://rpc.ankr.com/eth_goerli"

# Checks Balance
def check_balance(wallet):
    env = EnvPrivateKey(wallet)
    account: LocalAccount = Account.from_key(env.key)
    print('Address: ' + account.address)
    zksync_web3 = ZkSyncBuilder.build(ZKSYNC_PROVIDER)
    zk_balance = zksync_web3.zksync.get_balance(account.address, EthBlockParams.LATEST.value)
    print(f"Balance: {zk_balance}")


if __name__ == "__main__":
    for wallet in wallets:
        print(f"Checking balance for {wallet}:")
        check_balance(wallet)
        print()
