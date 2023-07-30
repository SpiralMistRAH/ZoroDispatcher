from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3

from zksync2.core.types import Token, EthBlockParams
from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.provider.eth_provider import EthereumProvider

PRIVATE_KEY = open("./private-keys/testnet-test-account.key", "r").read()
ZKSYNC_TEST_URL = "https://zksync2-testnet.zksync.dev"
RCP_ENDPOINT = "https://rpc.ankr.com/eth_goerli/<REDACTED API KEY>"

def deposit(amount: float):
    zksync = ZkSyncBuilder.build(ZKSYNC_TEST_URL)
    eth_web3 = Web3(Web3.HTTPProvider(RCP_ENDPOINT))
    account: LocalAccount = Account.from_key(PRIVATE_KEY)
    eth_provider = EthereumProvider(zksync, eth_web3, account)
    wei_amount = Web3.to_wei(amount, "ether")
    eth_token = Token.create_eth()
    gas_price = eth_web3.eth.gas_price
    before_deposit = eth_provider.get_l1_balance(eth_token, EthBlockParams.LATEST)

    print(f"Before: {before_deposit}")

    l1_tx_receipt = eth_provider.deposit(token=Token.create_eth(),
                                         amount=wei_amount,
                                         gas_price=gas_price)
    print(l1_tx_receipt)


if __name__ == "__main__":
    deposit(0.01)
