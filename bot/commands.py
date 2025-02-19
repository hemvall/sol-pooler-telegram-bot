from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes, CallbackContext, Updater
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.message import Message
from solders.system_program import transfer, TransferParams
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed
from spl.token.instructions import transfer as spl_transfer, get_associated_token_address
import base64
import json
import os

# https://api.mainnet-beta.solana.com/
# https://michaelhly.com/solana-py/
# https://solana.com/fr/docs/rpc/http
# Python (Flask/FastAPI)


# Constants
TOKEN: Final = '7923573769:AAGSP1_IcReEf8iLnvvEpwvSYAMwlVzsaMU'
BOT_USERNAME = '@SolPooler_v1_Bot.'

# Solana client setup
SOLANA_RPC_URL = "https://api.devnet.solana.com"
# https://api.mainnet-beta.solana.com
# https://api.testnet.solana.com
client = Client(SOLANA_RPC_URL)  # Use the mainnet or devnet endpoint

wallets_file_path = "secure_wallets/wallets.json"
def load():
    try:
        with open(wallets_file_path, "r") as file:
            wallets = json.load(file)
            return wallets
    except FileNotFoundError:
        print("Wallets file not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return []

def generate(update, context):
    nb_wallets: int = 3  # Change to 5 if needed
    wallets = []
    new_wallets = []
    user = update.message.from_user
    username = user.username
    os.makedirs(os.path.dirname(wallets_file_path), exist_ok=True)

    # Load existing data to append new wallets
    data = load_wallet_data()

    for i in range(nb_wallets):
        kp = Keypair()
        private_key = kp.secret()
        public_key = kp.pubkey()
        private_key_base64 = base64.b64encode(private_key + bytes(public_key)).decode('utf-8')

        new_wallets.append({"public_key": str(public_key), "private_key": private_key_base64})
        wallets.append(f"\n<b>💼 Wallet {i + 1}:</b>\n\n🔑 Private Key:\n{private_key_base64}\n\n")

    # Append new wallets to the existing ones
    data["wallets"].extend(new_wallets)

    # Save updated data
    with open(wallets_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    all_wallets_info = "".join(wallets)
    return update.message.reply_text(
        f"Here are your {nb_wallets} wallets:\n{all_wallets_info}Save these keys securely!",
        parse_mode='HTML'
    )

def balances(update, context):




def load_wallet_data():
    try:
        with open(wallets_file_path, "r") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            else:
                return {"wallets": [], "main_wallet": None}  # Initialize as a dictionary
    except FileNotFoundError:
        print("Wallets file not found.")
        return {"wallets": [], "main_wallet": None}  # Ensure structure
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return {"wallets": [], "main_wallet": None}