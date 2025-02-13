# SolPooler - Telegram Bot for Solana Trading

## 🚀 Overview
SolPooler is a Telegram bot designed to automate the creation of Solana addresses, receive funds, and execute token purchases using provided contract addresses (CA). This bot streamlines trading by simplifying the process of funding wallets and buying tokens automatically.

## 🔧 Features
- **Automatic SOL Address Creation**: Generates Solana addresses on demand.
- **Fund Management**: Receives SOL from your main wallet.
- **Automated Token Purchases**: Buys tokens using the specified contract address.
- **Secure Transactions**: Ensures smooth and secure fund transfers.
- **Telegram Command Interface**: Control the bot with simple commands.

## 💻 Commands

/create_wallets → Generates new SOL addresses

/balance → Checks wallet balances

/buy_token <contract_address> → Purchases tokens using the provided CA

/import_wallet → Import your main wallet that will provide funds

/transfer_funds <amount> <destination_address>

/withdraw_funds <amount>

## 🔒 Security Note
To keep your Telegram bot token secure, avoid hardcoding it in your scripts. Here is how you can do it :

Put .env file at root of project 

### Linux/macOS: Add this line to ~/.bashrc or ~/.zshrc
```export TELEGRAM_BOT_TOKEN="your-secret-token"```
### Windows (PowerShell):
```$env:TELEGRAM_BOT_TOKEN="your-secret-token"```

### in config.py
```
import os
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
```

Keep your .env file private to protect sensitive data.

Consider using a separate wallet for bot transactions to minimize risk.
