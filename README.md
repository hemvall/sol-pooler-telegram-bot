# SolPooler - Telegram Bot for Solana Trading
## 🚀 Overview
SolPooler is a Telegram bot designed to automate the creation of Solana addresses, receive funds, and execute token purchases using provided contract addresses (CA). This bot streamlines trading by simplifying the process of funding wallets and buying tokens automatically.
QuickNode - RPC

## 🔧 Features
- **Automatic SOL Address Creation**: Generates Solana addresses on demand.
- **Fund Management**: Receives SOL from your main wallet.
- **Automated Token Purchases**: Buys tokens using the specified contract address.
- **Secure Transactions**: Ensures smooth and secure fund transfers.
- **Telegram Command Interface**: Control the bot with simple commands.

### Showcase website :
- Main Page
![image](https://github.com/user-attachments/assets/2c6a2ffc-585f-4b72-aa57-ccb8c5b938e0)

- Functional Telegram Bot
   ![L7-MpitM](https://github.com/user-attachments/assets/64130ac2-72ca-400f-8a7d-3990ece76c20)
   ![GuJbDgr0](https://github.com/user-attachments/assets/4e72e8c3-486a-4847-ad75-be25e5731109)
   ![QRQ7krrx](https://github.com/user-attachments/assets/8350ace4-38b2-4255-8111-d86f782b0350)


- Online Bot simulator
  ![image](https://github.com/user-attachments/assets/1971f9d5-cf86-4370-af12-756633ee2369)
  ![image](https://github.com/user-attachments/assets/a6e9a60c-6418-4407-a6cf-3f450e0a303d)

## 💻 Commands

/create_wallets → Generates new SOL addresses

/balances → Checks wallet balances

/buy_token <contract_address> → Purchases tokens using the provided CA

/import_wallet → Import your main wallet that will provide funds

/transfer_funds <amount> <destination_address>

/withdraw_funds <amount>

### BotFather setcommands
start - Starts the bot  
balances - Checks wallet balances  
buy-token - Purchases tokens using the provided CA  
import_wallet - Import your main wallet to transfer funds to subwallets
transfer_funds - Transfers funds between wallets  
withdraw_funds - Send back funds from subwallet to your original one  
create_wallets - Creates 5 new Solana wallets  

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
