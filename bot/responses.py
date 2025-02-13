# responses.py
def handle_response(text: str) -> str:
    text = text.lower()

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

#########################################################################################
#########################################################################################
# /!\ could be useful later
#########################################################################################
#########################################################################################
def handle_wallet_creation(public_key: str, private_key_base64: str) -> str:
    return (
        f"New wallet created successfully!\n\n"
        f"Public Key: {public_key}\n\n"
        f"Private Key (Base64 encoded):\n{private_key_base64}\n\n"
        f"Be sure to save this information securely, as you will not be able to retrieve the private key again."
    )


def handle_balance_check(balance: float) -> str:
    if balance == 0:
        return "Your wallet balance is currently 0 SOL. Please top it up to start making transactions."
    else:
        return f"Your current wallet balance is {balance:.2f} SOL."


def handle_token_purchase(contract_address: str) -> str:
    return (
        f"Attempting to buy tokens from the contract at {contract_address}...\n\n"
        "Please ensure you have enough SOL to complete the transaction."
    )


def handle_transfer_funds(amount: float, recipient: str) -> str:
    if amount <= 0:
        return "Invalid transfer amount. Please specify a valid amount greater than 0 SOL."
    return (
        f"Transferring {amount:.2f} SOL to {recipient}...\n\n"
        "Please ensure the recipient address is correct before confirming."
    )
