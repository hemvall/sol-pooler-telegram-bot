from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes, CallbackContext, Updater
from solders.keypair import Keypair
from solana.rpc.api import Client
import base64
import json
import os

from bot.pump.pump_fun import *
from bot.solana_utils import *
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

wallets_file_path = "secure_wallets/user_{username}_wallets.json"
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


def generatewallets(update, context):
    nb_wallets: int = 3  # Change to 5 if needed
    wallets = []
    new_wallets = []
    user = update.message.from_user
    username = user.username

    # Construct the file path using the user's username
    user_wallets_file_path = wallets_file_path.format(username=username)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(user_wallets_file_path), exist_ok=True)

    # Load existing data to append new wallets
    data = load_wallet_data(user_wallets_file_path)

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
    with open(user_wallets_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    all_wallets_info = "".join(wallets)
    return update.message.reply_text(
        f"Here are your {nb_wallets} wallets:\n{all_wallets_info}Save these keys securely!",
        parse_mode='HTML'
    )

def load_wallet_data(file_path):
    try:
        with open(file_path, "r") as file:
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

async def balances(update, context):
    # Load wallets directly from the JSON file
    user = update.message.from_user
    username = user.username
    wallets_file_path = "secure_wallets/user_{username}_wallets.json"
    user_wallets_file_path = wallets_file_path.format(username=username)

    with open(user_wallets_file_path, "r") as file:
        data = json.load(file)  # Parse JSON
        wallets = data.get("wallets", [])  # Extract the list of wallets
        main_wallet = data.get("main_wallet", {})  # Extract the main wallet
    print(f"Main Wallet: {main_wallet}")
    print(f"Wallets loaded from {wallets_file_path}: {wallets}")

    EPSILON = 1e-9

    # Process main wallet if it exists
    if "public_key" in main_wallet:
        public_key = main_wallet["public_key"]
        public_key_final = Pubkey.from_string(public_key)
        response = client.get_balance(public_key_final)
        balance_sol = response.value / 1_000_000_000  # Convert lamports to SOL
        if abs(balance_sol) > EPSILON:
            await update.message.reply_text(f"<b>🌟 Main Wallet:</b> {balance_sol} SOL. ({public_key_final})", parse_mode='HTML')
        else:
            await update.message.reply_text(f"<b>🌟 Main Wallet:</b> 0 SOL ({public_key_final})\nYou don't have any money on this wallet, sir.", parse_mode='HTML')

    # Process subwallets if they exist
    count = 1
    for wallet in wallets:
        public_key = wallet["public_key"]
        public_key_final = Pubkey.from_string(public_key)  # Convert base58 string to Pubkey
        response = client.get_balance(public_key_final)
        balance_sol = response.value / 1_000_000_000  # Convert lamports to SOL
        if abs(balance_sol) > EPSILON:
            await update.message.reply_text(f"<b>💼 Wallet {count}:</b> {balance_sol} SOL. ({public_key_final})", parse_mode='HTML')
        else:
            await update.message.reply_text(
                f"<b>💼 Wallet {count}:</b> 0 SOL ({public_key_final})\nYou don't have any money on this wallet, sir.", parse_mode='HTML')

        count += 1

async def buytoken(update, context):
    # TODO : connect to each wallet and buy /!\ don't forget to make it random (which wallet)
    try:
        # Load keypair (you should securely manage private keys)
        user_keypair = Keypair()
        user_pubkey = user_keypair.pubkey()
        print(f"Generated wallet: {user_keypair}")
        mint_str = "7TmBExR2mUHx5gMiawV5F2eUQUTUrQMCjtvvSvRzpump"
        sol_in = .1
        slippage = 5
        await update.message.reply_text(f"🟢 Buying {sol_in} SOL worth of tokens {mint_str}.")
        buy(mint_str, sol_in, slippage)

        await update.message.reply_text(f"✅ ")

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("❌ Error during token purchase.")


async def transferfunds(update, context):
    await update.message.reply_text("🔄 Transferring funds...")
    kp = Keypair()
    with open(wallets_file_path, "r") as file:
        data = json.load(file)  # Parse JSON
        wallets = data.get("wallets", [])  # Extract the list of wallets
        main_wallet = data.get("main_wallet", {})  # Extract the main wallet

    recipients = []
    for wallet in wallets:
            public_key = wallet["public_key"]
            recipients.append({"pubkey":public_key, "amount":1000000})
    print(recipients)
    bundled_transaction = create_bundled_transaction(kp, recipients)
    result = send_bundled_transaction(bundled_transaction)

    print("Transaction ID:", result["result"])
    await update.message.reply_text(result["result"])

async def withdrawfunds(update, context):
    await update.message.reply_text("Transferring funds to your main wallet...")

    # Transaction details TODO : make it max amount
    amount_in_sol = 0.05
    lamports = int(amount_in_sol * 1_000_000_000)  # 1 SOL = 1e9 lamports

    with open(wallets_file_path, "r") as file:
        data = json.load(file)  # Parse JSON
        wallets = data.get("wallets", [])  # Extract the list of wallets
        main_wallet = data.get("main_wallet", {})  # Extract the main wallet
    # main wallet import
    recipient_private_key = main_wallet["private_key"]
    recipient_public_key = main_wallet["public_key"]

    # recipient's wallets import
    for wallet in wallets:
        sender_public_key = wallet["public_key"]
        print(f"Sending back {amount_in_sol} SOL from {sender_public_key} to your main Wallet...")
    await update.message.reply_text(f"✅ Successfully sent back {amount_in_sol} SOL to your main wallet from {sender_public_key} !➡️💸")

MENU, OPTION1, OPTION2, OPTION3, OPTION4 = range(5)
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🛠 Create Wallet", callback_data='create_wallets_command'),
         InlineKeyboardButton("💰 Check Balance", callback_data='balances_command')],

        [InlineKeyboardButton("💲 Buy Token", callback_data='buy_command'),
         InlineKeyboardButton("📤 Transfer Funds", callback_data='transfer_funds_command')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to SolPooler Bot! Choose an option:", reply_markup=reply_markup
    )
    return MENU
# Button click handler
async def button_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "create_wallets_command":
        await query.edit_message_text(text="Creating the wallets...")
        return OPTION1
    elif query.data == "balances_command":
        await query.edit_message_text(text="Checking your wallets...")
        return OPTION2
    elif query.data == "buy_command":
        await query.edit_message_text(text="Token purchase in progress...")
        return OPTION3
    elif query.data == "transfer_funds_command":
        await query.edit_message_text(text="Funds transfer in progress...")
        return OPTION4
    else:
        await query.edit_message_text(text="Unknown option selected.")
        return MENU

