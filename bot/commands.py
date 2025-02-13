from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from solana_utils import create_wallet

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛠 Create Wallet", callback_data='create_wallet')],
        [InlineKeyboardButton("💰 Check Balance", callback_data='check_balance')],
        [InlineKeyboardButton("💲 Buy Token", callback_data='buy_token')],
        [InlineKeyboardButton("📤 Transfer Funds", callback_data='transfer_funds')],
        [InlineKeyboardButton("📤 Start Bot", callback_data='transfer_funds')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to SolPooler Bot! Choose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "create_wallet":
        await create_wallets_command(update, context)
    elif query.data == "check_balance":
        await balances_command(update, context)
    elif query.data == "buy_token":
        await query.message.reply_text("Send the contract address like this: /buy_token <contract_address>")
    elif query.data == "transfer_funds":
        await transfer_funds_command(update, context)

async def create_wallets_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    public_key, private_key_base64 = create_wallet()
    await update.message.reply_text(
        f"New wallet created!\n\n"
        f"Public Key: {public_key}\n\n"
        f"Private Key:\n{private_key_base64}\n\n"
        f"Save this key securely!"
    )

async def balances_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You don't have a lot of money, sir.")

async def buy_token_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 1:
        contract_address = context.args[0]
        await update.message.reply_text(f"Buying token at contract {contract_address}...")
    else:
        await update.message.reply_text("Usage: /buy_token <contract-address>")

async def transfer_funds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Transferring funds...")