from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN
from commands import create_wallets_command, balances_command, buy_token_command, transfer_funds_command
from responses import handle_response

def start_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("create_wallets", create_wallets_command))
    application.add_handler(CommandHandler("balances", balances_command))
    application.add_handler(CommandHandler("buy_token", buy_token_command))
    application.add_handler(CommandHandler("transfer_funds", transfer_funds_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)
    application.run_polling()

async def handle_message(update, context):
    response = handle_response(update.message.text)
    await update.message.reply_text(response)

async def error(update, context):
    print(f'Update {update} caused error {context.error}')
