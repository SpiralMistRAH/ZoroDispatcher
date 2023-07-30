import asyncio
from web3 import Web3, HTTPProvider, Account
from zksync_sdk import ZkSyncProviderV01, HttpJsonRPCTransport, network, ZkSync, EthereumProvider, Wallet, ZkSyncSigner, EthereumSignerWeb3, ZkSyncLibrary
from decimal import Decimal

#TODO fix await error

# Load Crypto Library
library = ZkSyncLibrary()

# Create Zksync Provider
provider = ZkSyncProviderV01(provider=HttpJsonRPCTransport(network=network.goerli)) # using test network

# Setup web3 acc
account = Account.from_key("PRIVATE_KEY")

# Create EthereumSigner
ethereum_signer = EthereumSignerWeb3(account=account) #using existing acc

# Create wallet
signer_v1 = ZkSyncSigner.from_account(account, library, network.goerli.chain_id) # test network
# Initialization from zksync seed
signer_v2 = ZkSyncSigner.from_seed(library, b"seed")
# Initialization from zksync private key
signer_v3 = ZkSyncSigner(library, b"private_key")

contracts = await provider.get_contract_address()

w3 = Web3(HTTPProvider(endpoint_uri="GETH_ENDPOINT" ))

# Setup zksync contract interactor
zksync = ZkSync(account=account, web3=w3,
                zksync_contract_address=contracts.main_contract)
# Create ethereum provider for interacting with ethereum node
ethereum_provider = EthereumProvider(w3, zksync)

# Initialize zksync signer, all creating options were described earlier
signer = ZkSyncSigner.from_account(account, library, network.goerli.chain_id)
# Initialize Wallet
wallet = Wallet(ethereum_provider=ethereum_provider, zk_signer=signer,
                eth_signer=ethereum_signer, provider=provider)

# Find token for depositing
token = await wallet.resolve_token("USDT")
# Approve Enough deposit using token contract
await wallet.ethereum_provider.approve_deposit(token, Decimal(1))

# Deposit money from contract to our address
deposit = await wallet.ethereum_provider.deposit(token, Decimal(1),
                                                 account.address)