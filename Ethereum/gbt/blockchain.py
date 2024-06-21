from web3 import Web3


def send_tx(sender, receiver, amount, web3):
    """
    Method for sending a transaction in (the private) ETH-Blockchain.

    :param sender:  private key from sending account
    :param receiver: hash value of the pub-key of the recipient as a string
                    (i.e: '0xf54DFE141A3a02BD6a0a85d50360B044449C9aB5')
    :param amount: amount of wei you want to send
    :param web3:  Instance of web3 connection to a node. Defines to which blockchain is connected and which methods
                  are available.
    :return:
    """
    account = web3.eth.account.from_key(sender)

    # create tx
    signed_txn = web3.eth.account.sign_transaction(dict(
        nonce=web3.eth.get_transaction_count(account.address),
        chainId=108,
        gasPrice=web3.eth.gas_price,
        gas=100000,
        to=receiver,
        value=amount,
        data=b'',
    ),
        account._private_key,
    )

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash


def read_tx(tx_hash, web3):
    tx = web3.eth.get_transaction(tx_hash)
    _data = tx.input
    return web3.to_text(_data)


class GBT:

    def __init__(self, rpc_url=''):
        self.w1 = Web3(Web3.HTTPProvider('http://62.171.152.173:9001'))
        self.w2 = Web3(Web3.HTTPProvider('http://144.91.79.46:9001'))
        self.w3 = Web3(Web3.HTTPProvider('http://144.91.79.79:9001'))
        if rpc_url != '':
            self.w4 = Web3(Web3.HTTPProvider(rpc_url))
