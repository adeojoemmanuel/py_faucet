from web3 import Web3
from django.conf import settings

def get_web3():
    return Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))

def send_eth(wallet_address):
    w3 = get_web3()
    account = w3.eth.account.from_key(settings.SENDER_PRIVATE_KEY)
    
    tx = {
        'to': wallet_address,
        'value': w3.to_wei(0.0001, 'ether'),
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(account.address),
        'chainId': 11155111  # Sepolia
    }
    
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()