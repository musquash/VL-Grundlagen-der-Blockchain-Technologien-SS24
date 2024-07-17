"""
Hilfestellung zu den Aufgaben im Übungsblatt 6 der Vorlesung Grundlagen der Blockchain-Technologien im Sommersemester 24
"""

from Ethereum.gbt.blockchain import GBT, send_tx, read_tx, get_block_with_most_transactions, get_largest_block, \
                                    find_pgp_keys, send_tx_data

# First you have to init an instance. You can connect to your own node by put in the RPC information:
# GBT('http://<url.com|IP>:<port>)
gbt = GBT()

# You can check, if the connection to the node is possible
print(f"Node 1 ist verbunden: {gbt.w1.is_connected()} \n"
      f"Node 2 ist verbunden: {gbt.w2.is_connected()} \n"
      f"Node 3 ist verbunden: {gbt.w3.is_connected()}")

# For sending a transaction you first need an account. You can import it from a private key or just create a fresh new
# account. Make sure to save the private key to be able to retore the account if you restart the program. Otherwise a
# new accoutnt with again no funds will be created:
account = gbt.w1.eth.account.create("exercise")
account_from_key = gbt.w1.eth.account.from_key(account._private_key)

print(f"You have an account with address {account.address} \n"
      f"and prviate key {account._private_key}")
print(f"You have an imported account with address {account_from_key.address} \n"
      f"and prviate key {account_from_key._private_key}")

# Exercise 6.1 b a:
block_100 = gbt.w1.eth.get_block(100)
print(f"Block 100 has hash-ID: {block_100.hash.hex()}")


# Now the transaction must be initialized and sent from an account with a balance.
tx_hash = send_tx(sender=account._private_key, receiver=account.address, web3=gbt.w1, amount=10000)

print(f"Transaction with hash {tx_hash} was successfully deployed.")


# Exercise 6.1 b b:
# You have to extend the send_tx the nonce paramter with "pending". This option helps to handle the creation and of Tx
# and sum up the nonce field even for not included Txs in the blockchain. Then a for loop is possible.
for step in range(1000):
      send_tx(sender=account._private_key, receiver=account.address, web3=gbt.w1, amount=1000)


# Exercise 6.1 b c:
gbt.w1.eth.get_block_number()
highest_tx_count, highest_tx_blocks = get_block_with_most_transactions(gbt.w1, start=0)

print(f"You will find {highest_tx_count} txs in blocks: {highest_tx_blocks}")

largest_gas_limit, largest_blocks = get_largest_block(gbt.w1, start=8000)
print(f"With a gas limit of {largest_gas_limit} you will find biggest blocks in {largest_blocks}")


# Exercise 6.1 b d:
# get the pgp key by loading or just pasting it.
pgp = """-----BEGIN PGP PUBLIC KEY BLOCK-----

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
I6u8MdjcsXURKg==
=9Yqa
-----END PGP PUBLIC KEY BLOCK-----"""

# Now sending the pgp key to the blockchain.
receipt = send_tx_data(sender=account._private_key, receiver=account.address, amount=1000, web3=gbt.w1, text=pgp)


# Exercise 6.1 b e:
# The following method finds all pgp keys, but don't compare if it is already saved.
keys = find_pgp_keys(w3=gbt.w1, start=110000)


