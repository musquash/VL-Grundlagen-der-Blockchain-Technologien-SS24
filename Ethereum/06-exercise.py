"""
Hilfestellung zu den Aufgaben im Übungsblatt 6 der Vorlesung Grundlagen der Blockchain-Technologien im Sommersemester 24
"""

from Ethereum.gbt.blockchain import GBT, send_tx, read_tx

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


# Now the transaction must be initialized and sent from an account with a balance.
tx_hash = send_tx(sender=account._private_key, receiver=account.address, web3=gbt.w1, amount=10000)

print(f"Transaction with hash {tx_hash} was successfully deployed.")


# Read data from a transaction
tx_hash = '0xd465c580999e9b40afcdb21a4eb3719f0c95218b351dbe9ac1f268cbd12b1529'
read_tx(f"In Tx with ID {tx_hash} is follwing text: \n",  f"{gbt.w1}")





