from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, Updater
from solders.keypair import Keypair
from solana.rpc.api import Client
import base64

# https://api.mainnet-beta.solana.com/
# https://michaelhly.com/solana-py/
# https://solana.com/fr/docs/rpc/http
# Python (Flask/FastAPI)

# Constants
TOKEN: Final = '7923573769:AAGSP1_IcReEf8iLnvvEpwvSYAMwlVzsaMU'
BOT_USERNAME = '@SolPooler_v1_Bot.'

# Solana client setup
client = Client("https://api.mainnet-beta.solana.com/")  # Use the mainnet or devnet endpoint


# Commands
async def create_wallets_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO : ask for number of wallets I want to create
    # Generate a new Solana wallet
    kp = Keypair()

    private_key = kp.secret()
    public_key = kp.pubkey()
    public_key_bytes = bytes(public_key)
    public_key = public_key
    full_private_key = private_key + public_key_bytes
    private_key_base64 = base64.b64encode(full_private_key).decode('utf-8')
    await update.message.reply_text(
        f"New wallet created!\n\n"
        f"Public Key: {public_key}\n\n"
        f"Private Key:\n{private_key_base64}\n\n"
        f"Save this key securely!"
    )
    # NOTE: Private key should never be exposed in production! This is just for demonstration purposes.
    # If you need to store or manage the private key, you should do it securely.

async def balances_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You don't have a lot of money, sir.")

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

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'Hey there!'
    if 'hey' in processed:
        return 'Hello there!'
    return 'I do not understand..'

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

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)
    print('Polling telegram bot...')
    app.run_polling(poll_interval=3)
