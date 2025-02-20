from mailbox import Message

import solders.solders
from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.instruction import Instruction
from solders.hash import Hash
from solders.message import Message
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed
from solders.signature import Signature
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.keypair import Keypair

from solders.transaction import VersionedTransaction
from solana.rpc.api import Client
from bot.config import SOLANA_RPC_URL, PRIV_KEY
import base64
client = Client(SOLANA_RPC_URL)

def create_wallet():
    kp = Keypair()
    private_key = kp.secret()
    public_key = kp.pubkey()
    public_key_bytes = bytes(public_key)
    full_private_key = private_key + public_key_bytes
    private_key_base64 = base64.b64encode(full_private_key).decode('utf-8')
    return public_key, private_key_base64

def create_bundled_transaction(sender_keypair, recipients):
    recent_blockhash = client.get_latest_blockhash().value
    program_id = Pubkey.default()
    arbitrary_instruction_data = bytes([1])
    accounts = []
    instruction = Instruction(program_id, arbitrary_instruction_data, accounts)
    print(f"INSTRUCTION : {instruction}")
    payer = Keypair()
    message = Message([instruction], payer.pubkey())
    print(f"MESSAGE : {message}")
    print(f"keypairs : {sender_keypair}")
    tx = Transaction(from_keypairs=[sender_keypair], message=message,recent_blockhash=recent_blockhash.blockhash)
    print(f"Tx : {tx}")
    tx.recent_blockhash = recent_blockhash
    tx.fee_payer = sender_keypair.public_key

    tx.sign(sender_keypair)
    return tx

def send_bundled_transaction(transaction, recipients):
    # Convert transaction en VersionedTransaction (utilisé par solders)
    versioned_tx = VersionedTransaction.from_legacy_transaction(transaction)
    opts = TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)
    result = client.send_transaction(versioned_tx, opts=opts)
    return result