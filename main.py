from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes, CallbackContext, Updater
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
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
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
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
    contract_address: str = ''
    if len(context.args) == 1:  # Verify if the parameter is present
        contract_address = context.args[0]
        await update.message.reply_text(f"The purchase order for the contract {contract_address} is in progress..")
    else:
        await update.message.reply_text("Invalid input. Please try again with a valid contract address.\n\n/buy_token <insert-token-CA>")
    # TODO : connect to each wallet and buy /!\ don't forget to make it random (which wallet)

async def transfer_funds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Transferring funds to your wallets...")


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
            "/buy_token <contract-address> - Buy a token from a provided contract address\n"
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
            "To buy a token, use the /buy_token <contract-address> command.\n"
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
    app.add_handler(CommandHandler('buy_token', buy_token_command))
    app.add_handler(CommandHandler('transfer_funds', transfer_funds_command))
    app.add_handler(CommandHandler('import_wallet', import_wallet_command))
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)
    print('Polling telegram bot...')
    app.run_polling(poll_interval=3)
