from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes, CallbackContext, Updater
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solana.rpc.api import Client
import spl.token.instructions as spl_token
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solana.rpc.commitment import Commitment
import requests
import base64
import base58
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


# Commands

def load_wallets():
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


async def create_wallets_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text(
        f"Here are your {nb_wallets} wallets:\n{all_wallets_info}Save these keys securely!",
        parse_mode='HTML'
    )


async def balances_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Load wallets directly from the JSON file
    with open(wallets_file_path, "r") as file:
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


async def buy_token_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO : connect to each wallet and buy /!\ don't forget to make it random (which wallet)
    # Load wallet
    private_key = "34nA4uSZrb3se1jPRCCn6NqPLBiMg5nNS5DMRrzk1hzBvUxF9qej47RhuXrPJEADcEqEVa3hndtPDVCJcoDu4ChD"  # Replace with your private key
    private_key_bytes = base58.b58decode(private_key)
    wallet = Keypair.from_bytes(private_key_bytes)

    # Get the latest blockhash
    latest_blockhash = client.get_latest_blockhash().value.blockhash

    # Example: Swap via Jupiter API (simplified)
    JUPITER_API = "https://quote-api.jup.ag/v6/quote"
    INPUT_MINT = "So11111111111111111111111111111111111111112"  # SOL
    OUTPUT_MINT = "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU"  # Example USDC on Devnet
    AMOUNT_IN = 10000000  # Amount in lamports (0.01 SOL)

    quote_response = requests.get(
        f"{JUPITER_API}?inputMint={INPUT_MINT}&outputMint={OUTPUT_MINT}&amount={AMOUNT_IN}&slippageBps=50"
    )
    quote = quote_response.json()
    print(quote)  # Debugging step

    # Get swap transaction from Jupiter
    swap_tx = requests.post(
        "https://quote-api.jup.ag/v6/swap",
        json={
            "quoteResponse": quote,
            "userPublicKey": str(wallet.pubkey()),
            "wrapAndUnwrapSol": True,
        }
    ).json()
    print(swap_tx)

    # Deserialize transaction
    encoded_tx = swap_tx["swapTransaction"]
    decoded_tx = base64.b64decode(encoded_tx)
    transaction = VersionedTransaction.from_bytes(decoded_tx)

    # Sign transaction
    signed_tx = transaction.sign([wallet])

    # Send transaction
    response = client.send_transaction(signed_tx, commitment=Commitment("confirmed"))

    print(f"Transaction ID: {response.value}")

async def transfer_funds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Transferring funds...")
    sender_public_key = Pubkey.from_string("9dqa3aPW8B8FdkvhBWFBvXZs5TKWeyYPidLzRzWrhq7M")
    sender_private_key = "Z0rgDd7M+5upSDou0ofm84PkD6AsKiI9eVN/t3JMM0OATVKP3EJ0zYO0c4i3JxHznZBXMRJO/5rOhg6+idrg4A=="
    receiver_public_key = "3khUiiKtVTe5kV8t7ybZ9E3dMWa1FoNCJRtwYCi8ECm4"
    receiver_public_key = "2tFbFhbiDVYLUeC5/7qjqYKk2cQctFC3ajOknrL0UIko6R3+0g7E3JfcVaTHYg1wNP4KAajM++4MpbbwTlOG3w=="
    try:
        sender_private_key_bytes = base64.b64decode(sender_private_key)
        if len(sender_private_key_bytes) != 64:
            raise ValueError("Private key size must be 64 bytes.")
    except Exception as e:
        print(f"Error decoding private key: {e}")
        exit()
    # Connect to the Solana devnet or mainnet
    rpc_url = "https://api.devnet.solana.com"
    client = Client(rpc_url)

    # Get the sender's balance (this step is optional, just to check before the transfer)
    sender_balance = client.get_balance(sender_public_key)
    print(f"Sender balance: {sender_balance['result']['value']} SOL")

    # Transfer amount in SOL
    amount = 0.1  # amount to transfer

    # Create the transaction
    transaction = Transaction()
    transaction.add(
        TransferParams.transfer(
            sender_public_key,
            receiver_public_key,
            amount * 10 ** 9  # Amount in lamports (1 SOL = 10^9 lamports)
        )
    )

    # Sign the transaction with the sender's keypair
    transaction.sign(sender_private_key)

    # Send the transaction to the network
    response = client.send_transaction(transaction, sender_private_key)

    # Confirm the transaction
    signature = response['result']
    confirmation = client.confirm_transaction(signature)
    print(f"Transaction confirmed with signature: {signature}")
async def withdraw_funds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
async def start_command(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("🛠 Create Wallet", callback_data='create_wallets_command'),
         InlineKeyboardButton("💰 Check Balance", callback_data='balances_command')],

        [InlineKeyboardButton("💲 Buy Token", callback_data='buy_token_command'),
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
    elif query.data == "buy_token_command":
        await query.edit_message_text(text="Token purchase in progress...")
        return OPTION3
    elif query.data == "transfer_funds_command":
        await query.edit_message_text(text="Funds transfer in progress...")
        return OPTION4
    else:
        await query.edit_message_text(text="Unknown option selected.")
        return MENU

# Responses
def handle_response(text: str) -> str:
    text: str = text.lower()
    if 'hello' in text or 'hi' in text:
        return "Hey there! How can I assist you today?"
    elif 'hey' in text:
        return "Hello! What can I help you with?"

    elif 'help' in text:
        return (
            "I can help you with the following commands:\n\n"
            "/create_wallets - Create a new Solana wallet\n"
            "/balances - Check your current wallet balance\n"
            "/buy <contract-address> - Buy a token from a provided contract address\n"
            "/transfer_funds - Transfer funds to a new address\n"
            "Just type a command to get started!"
        )

    elif 'wallet' in text:
        return (
            "To create a new Solana wallet, use the /create_wallets command.\n"
            "This will generate a new wallet for you, including a public and private key."
        )

    elif 'token' in text:
        return (
            "To buy a token, use the /buy <contract-address> command.\n"
            "Just provide the contract address to proceed with the purchase!"
        )

    elif 'balance' in text:
        return (
            "Use the /balances command to check your current Solana wallet balance. "
            "Make sure to have a wallet set up before checking your balance."
        )

    elif 'transfer' in text or 'send' in text:
        return (
            "To transfer funds, use the /transfer_funds command.\n"
            "Make sure you provide the correct recipient address to avoid mistakes."
        )

    return (
        "I’m not sure I understand. You can type /help to see the list of commands I can help with."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) type: {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Conversation states
ASK_PUBLIC_KEY, ASK_PRIVATE_KEY = range(2)


async def import_wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the conversation to import a main wallet by asking for the public key."""
    await update.message.reply_text("Please enter your main wallet's public key:")
    return ASK_PUBLIC_KEY  # Move to the next state


async def ask_private_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the public key input and asks for the private key."""
    context.user_data["public_key"] = update.message.text  # Store public key

    print(f"Received Public Key: {context.user_data['public_key']}")  # Debugging log
    print(f"Current state: ASK_PUBLIC_KEY")  # Check if state transitions correctly

    await update.message.reply_text("Now, please enter your main wallet's private key:")
    return ASK_PRIVATE_KEY  # Move to the next state



async def save_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    private_key = update.message.text
    public_key = context.user_data.get("public_key")

    if not public_key:
        await update.message.reply_text("Error: Public key was not provided. Please restart the import process.")
        return ConversationHandler.END

    # Load existing data
    data = load_wallet_data()

    # Store or update main wallet
    data["main_wallet"] = {"public_key": public_key, "private_key": private_key}

    # Save updated data
    with open(wallets_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    await update.message.reply_text("✅ Main wallet successfully imported!")
    return ConversationHandler.END



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the wallet import process."""
    await update.message.reply_text("Wallet import canceled.")
    return ConversationHandler.END

if __name__ == '__main__':
    print('Starting telegram bot...')
    app = Application.builder().token(TOKEN).build()
    import_wallet_conversation = ConversationHandler(
        entry_points=[CommandHandler('import_wallet', import_wallet_command)],
        states={
            ASK_PUBLIC_KEY: [MessageHandler(filters.TEXT, ask_private_key)],
            ASK_PRIVATE_KEY: [MessageHandler(filters.TEXT, save_wallet)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Commands
    app.add_handler(import_wallet_conversation)
    app.add_handler(CommandHandler('create_wallets', create_wallets_command))
    app.add_handler(CommandHandler('balances', balances_command))
    app.add_handler(CommandHandler('buy', buy_token_command))
    app.add_handler(CommandHandler('transfer_funds', transfer_funds_command))
    app.add_handler(CommandHandler('withdraw_funds', withdraw_funds_command))
    app.add_handler(CommandHandler('import_wallet', import_wallet_command))
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)
    print('Polling telegram bot...')
    app.run_polling(poll_interval=3)
