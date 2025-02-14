from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, CallbackContext, Updater
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


async def create_wallets_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nb_wallets: int = 5
    wallets = []
    wallets_keys = []
    os.makedirs(os.path.dirname(wallets_file_path), exist_ok=True)

    # Generate the new Sol wallets
    for i in range(nb_wallets):
        kp = Keypair()

        private_key = kp.secret()
        public_key = kp.pubkey()
        public_key_bytes = bytes(public_key)
        full_private_key = private_key + public_key_bytes
        private_key_base64 = base64.b64encode(full_private_key).decode('utf-8')

        wallets.append(
            f"\n<b>💼 Wallet {i + 1}:</b>\n\n"
            # f"🔑 Public Key {public_key}\n"
            f"🔑 Private Key:\n{private_key_base64}\n\n"
        )
        # TODO : convert to pubkey correctly
        wallets_keys.append({
            "public_key": Pubkey(public_key),
            "private_key": private_key_base64
        })

    # Combine all wallet info into one message and send it
    all_wallets_info = "".join(wallets)
    await update.message.reply_text(
        f"Here are your {nb_wallets} wallets:\n{all_wallets_info}Save these keys securely!\n\n💡The wallets will automatically be imported into the bot, and you can also add them manually to your Phantom wallet.",
        parse_mode='HTML'
    )
    # Save wallet keys to
    with open(wallets_file_path, 'w') as file:
        json.dump(wallets_keys, file, indent=4)

    print(f"Wallets saved to {wallets_file_path}")
    # NOTE: Private keys should never be exposed in production! This is just for demonstration purposes.
    # If you need to store or manage the private key, you should do it securely.


async def balances_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Wallets loaded from {wallets_file_path}")
    wallets = load_wallets()
    print(wallets)
    print(wallets[0])
    count = 1
    for wallet in wallets:
        public_key = wallet["public_key"]

        # use pubkey_obj to get balance
        response = client.get_balance(public_key)
        balance_sol = response["result"]["value"] / 1_000_000_000

        EPSILON = 1e-9  # Almost 0
        if abs(balance_sol) > EPSILON:
            await update.message.reply_text(f"Wallet {count} : {balance_sol} SOL.")
        else:
            await update.message.reply_text("You don't have any money, sir.")

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

if __name__ == '__main__':
    print('Starting telegram bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('create_wallets', create_wallets_command))
    app.add_handler(CommandHandler('balances', balances_command))
    app.add_handler(CommandHandler('buy_token', buy_token_command))
    app.add_handler(CommandHandler('transfer_funds', transfer_funds_command))
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)
    print('Polling telegram bot...')
    app.run_polling(poll_interval=3)
