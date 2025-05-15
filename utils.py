# utils.py
import logging
from datetime import datetime

# Configure logging for debugging and error tracking
def configure_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def log_transaction(transaction):
    logging.info(f"Transaction: {transaction.sender} -> {transaction.recipient} | Amount: {transaction.amount}")

def log_block(block):
    logging.info(f"Block mined: Index {block.index} | Hash {block.hash} | Prev Hash {block.previous_hash}")

def validate_address(address):
    """ Utility to validate the format of the address """
    if len(address) != 42 or not address.startswith("0x"):
        raise ValueError("Invalid address format. It should be a 42-character string starting with '0x'.")
    return True

def format_timestamp():
    """ Format the current timestamp for blocks and transactions """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_transaction_data(sender, recipient, amount):
    """ Format transaction data for easier debugging or display """
    return f"Sender: {sender}, Recipient: {recipient}, Amount: {amount}"

def validate_transaction(transaction):
    """ Validate the transaction (e.g., check if the amount is positive) """
    if transaction.amount <= 0:
        raise ValueError("Transaction amount must be greater than zero.")
    if not validate_address(transaction.sender) or not validate_address(transaction.recipient):
        raise ValueError("Invalid address format.")
    return True
