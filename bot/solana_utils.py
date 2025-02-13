from solders.keypair import Keypair
import base64
from solana.rpc.api import Client
from config import SOLANA_RPC_URL

client = Client(SOLANA_RPC_URL)

def create_wallet():
    kp = Keypair()
    private_key = kp.secret()
    public_key = kp.pubkey()
    public_key_bytes = bytes(public_key)
    full_private_key = private_key + public_key_bytes
    private_key_base64 = base64.b64encode(full_private_key).decode('utf-8')
    return public_key, private_key_base64