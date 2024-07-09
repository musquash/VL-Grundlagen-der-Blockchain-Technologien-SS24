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
        nonce=web3.eth.get_transaction_count(account.address, "pending"), # This pending allows to send consecutive txs.
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


def get_block_with_most_transactions(w3, start=0):
    highest_tx_count = 0
    highest_tx_blocks = []

    # Gehe durch alle Blöcke
    latest_block = w3.eth.block_number
    for block_number in range(start, latest_block + 1):
        if (block_number % 1000) == 0:
            print(f"We are currently investigating block: {block_number}")
        block = w3.eth.get_block(block_number)
        tx_count = len(block.transactions)

        if tx_count > highest_tx_count:
            highest_tx_count = tx_count
            highest_tx_blocks = [block_number]
        elif tx_count == highest_tx_count:
            highest_tx_blocks.append(block_number)

    return highest_tx_count, highest_tx_blocks


def get_largest_block(w3, start=0):
    largest_gas_limit = 0
    largest_blocks = []
    block_number = w3.eth.get_block_number()

    # Gehe durch alle Blöcke
    for block_number in range(start, block_number + 1):
        if (block_number % 1000) == 0:
            print(block_number)
        block = w3.eth.get_block(block_number)
        gas_limit = block.gasLimit

        if gas_limit > largest_gas_limit:
            largest_gas_limit = gas_limit
            largest_blocks = [block_number]
        elif gas_limit == largest_gas_limit:
            largest_blocks.append(block_number)

    return largest_gas_limit, largest_blocks


def send_tx_data(sender, receiver, amount, web3, text=''):
    """
    Method for sending a transaction in (the private) ETH-Blockchain, with an optional text message.

    :param sender:  private key from sending account
    :param receiver: hash value of the pub-key of the recipient as a string (i.e: '0xf54DFE141A3a02BD6a0a85d50360B044449C9aB5')
    :param amount: amount of wei you want to send
    :param web3:  Instance of web3 connection to a node. Defines to which blockchain is connected and which methods are available.
    :param text: text message to include in the transaction (optional)
    :return: transaction hash
    """
    account = web3.eth.account.from_key(sender)

    # Encode the text message as bytes
    data = text.encode('utf-8')

    # Create the transaction
    signed_txn = web3.eth.account.sign_transaction(dict(
        nonce=web3.eth.get_transaction_count(account.address, 'pending'),
        chainId=108,
        gasPrice=web3.eth.gas_price,
        gas=1000000,
        to=receiver,
        value=amount,
        data=data,
    ), account._private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash


def find_pgp_keys(w3, start=0):
    pgp_keys_with_tx_ids = []

    latest_block = w3.eth.block_number
    for block_number in range(start, latest_block + 1):
        if block_number % 1000 == 0:
            print(f"We are currently investigating block: {block_number}")
        block = w3.eth.get_block(block_number, full_transactions=True)
        for tx in block.transactions:
            text = read_tx(tx.hash, w3)
            if len(text) >= 35:
                if text[0:35] == '-----BEGIN PGP PUBLIC KEY BLOCK----':
                    pgp_keys_with_tx_ids.append((tx.hash.hex(), text))

    return pgp_keys_with_tx_ids


class GBT:

    def __init__(self, rpc_url=''):
        self.w1 = Web3(Web3.HTTPProvider('http://62.171.152.173:9001'))
        self.w2 = Web3(Web3.HTTPProvider('http://144.91.79.46:9001'))
        self.w3 = Web3(Web3.HTTPProvider('http://144.91.79.79:9001'))
        if rpc_url != '':
            self.w4 = Web3(Web3.HTTPProvider(rpc_url))
