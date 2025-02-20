from bot.commands import *
from bot.responses import *

# Commands
def load_wallets():
    load()
async def create_wallets_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await generatewallets(update, context)
async def balances_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await balances(update, context)
async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await buytoken(update, context)
async def transfer_funds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await transferfunds(update, context)
async def withdraw_funds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await withdrawfunds(update, context)
async def start_command(update: Update, context: CallbackContext) -> int:
    await start(update, context)

# Responses
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

    # Retrieve the user's username
    user = update.message.from_user
    username = user.username
    wallets_file_path = "secure_wallets/user_{username}_wallets.json"
    # Construct the file path using the user's username
    user_wallets_file_path = wallets_file_path.format(username=username)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(user_wallets_file_path), exist_ok=True)

    # Load existing data
    data = load_user_wallet_data(user_wallets_file_path)

    # Store or update main wallet
    data["main_wallet"] = {"public_key": public_key, "private_key": private_key}

    # Save updated data
    with open(user_wallets_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    await update.message.reply_text("✅ Main wallet successfully imported!")
    return ConversationHandler.END

def load_user_wallet_data(file_path):
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
    app.add_handler(CommandHandler('buy', buy_command))
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
