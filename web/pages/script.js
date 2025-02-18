const commands = [
    "/create_wallets",
    "/balances",
    "/buy_token",
    "/import_wallet",
    "/transfer_funds",
    "/withdraw_funds"
];
const wallets = [
    "3hU6AvxS1uQHtHpY7oycLrEb5jYNHkT8ZjNzPsnCxZTJ",
    "GxjZ8N9eZJc8Xo26Mwd6moxv5RR9KK1AixVCu46VKzXH",
    "HkJ8XzPbByosNRcXoY71q1Gv8nMnErANPsSA62VAUnwb",
    "EKNfGqZC2T8CqG9fJ7uKZwzjP2VfVCZShTR9UxEYvAzM",
    "4mB5xCVdsNU6L1s5KQ87YhZpNk5T7yqD8RTpFh9XABeT",
    "8yJqFZk6wLXW7pMoA3G5cRzQvT91NK2YVhMJC8PsaZTU",
    "Jz8Gv1YKZCo2Xw9tP5M7NRLqV63FAxTByps4UoE8dCZX",
    "Fp9KJzT7GxAqM8L12VRXYNWC5o46ZPbUo3dNsQvTpEJX",
    "N7ZpFJXMoLqY8RTAK5VCGx912W6pTo3dMUoQvEyJs4bC",
    "5XWJzGqKMoV8T7N29pFYLQAo6ZR3PC1UoNTMdCE4xsBY",
    "L9XTA7pFZJqGoY2WVKM83N5oQdR16PToCUoNTMJs4XCBE",
    "2VpFJqXMoG8W7NZ9TAL5YKQTRC16PoUoNTMdCEoXs4JBY",
    "7XZpFJqMoV8TA5KWN9Y2GLQRC16PoUoNTMdCEoXs4JBYT",
    "Q7FJXMoV8TA5KWN9Y2GLZpRC16PoUoNTMdCEoXs4JBY"
];

function pickRandomWallets(wallets, count) {
    if (wallets.length < count) {
        throw new Error("Not enough wallets available.");
    }
    const shuffled = wallets.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
}

document.getElementById("cmdInput").addEventListener("input", function () {
    const input = this.value.trim().toLowerCase();
    const suggestionsBox = document.getElementById("suggestionsBox");

    if (input.startsWith("/")) {
        const filteredCommands = commands.filter(cmd => cmd.toLowerCase().startsWith(input));
        suggestionsBox.innerHTML = '';
        filteredCommands.forEach(cmd => {
            const suggestionItem = document.createElement("div");
            suggestionItem.textContent = cmd;
            suggestionItem.classList.add("suggestion-item");
            suggestionItem.onclick = () => {
                document.getElementById("cmdInput").value = cmd;
                suggestionsBox.style.display = 'none';
            };
            suggestionsBox.appendChild(suggestionItem);
        });
        suggestionsBox.style.display = filteredCommands.length ? 'block' : 'none';
    } else {
        suggestionsBox.style.display = 'none';
    }
});

document.getElementById("cmdInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        const input = this.value.trim();
        const outputDiv = document.querySelector(".output");

        if (input) {
            const newLine = document.createElement("div");
            newLine.classList.add("line");
            newLine.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">${input}</span>`;
            outputDiv.appendChild(newLine);

            // Handle the commands
            if (input === "/create_wallets") {
                const selectedWallets = pickRandomWallets(wallets, 3);

                const createWalletsText = document.createElement("div");
                createWalletsText.classList.add("line");
                createWalletsText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span>Here are your 3 new wallets:` +
                    selectedWallets.map(wallet => `<br>${wallet}`).join("") + "<br>💡 They have been imported into your account";

                outputDiv.appendChild(createWalletsText);
            } else if (input === "/balances") {
                const balancesText = document.createElement("div");
                balancesText.classList.add("line");
                balancesText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">🌐 Main Wallet (RS6A...47KD): 8.61 SOL<br>💼 SubWallet 1 (L9XT...XCBE): 5.21 SOL<br>💼 SubWallet 2 (C0XZ...T5U7): 0.08 SOL</span>`;
                outputDiv.appendChild(balancesText);
            } else if (input === "/buy_token") {
                function getUserInput() {
                    return new Promise((resolve) => {
                        const userInput = prompt("Please provide the token CA you want to buy : ");
                        resolve(userInput);
                    });
                }
                
                // Function needs to be async to use await
                async function handleBuyToken() {
                    // Ask for the token name or quantity before purchasing
                    const tokenPromptText = document.createElement("div");
                    tokenPromptText.classList.add("line");
                    tokenPromptText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Please provide the token CA you want to buy.Please provide the token CA you want to buy </span>`;
                    outputDiv.appendChild(tokenPromptText);

                    // Wait for the user to input the token name/quantity
                    const tokenInput = await getUserInput(); // You'd need to define getUserInput to capture user input

                    // Assuming tokenInput is valid, proceed with purchasing
                    const buyTokenText = document.createElement("div");
                    buyTokenText.classList.add("line");
                    buyTokenText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Successfully purchased the token with your wallets (${tokenInput})</span>`;
                    outputDiv.appendChild(buyTokenText);
                }

                // Call the async function
                handleBuyToken();
            } else if (input === "/import_wallet") {
                const importWalletText = document.createElement("div");
                importWalletText.classList.add("line");
                importWalletText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Please provide your wallet's Public and Private keys.</span>`;
                outputDiv.appendChild(importWalletText);
            } else if (input.startsWith("/transfer_funds")) {
                const transferFundsText = document.createElement("div");
                transferFundsText.classList.add("line");
                const destination = input.split(" ")[1] || "No address provided";
                transferFundsText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Successfully transferred 0.1 SOL to each of your SOL subwallets ${destination}.</span>`;
                outputDiv.appendChild(transferFundsText);
            } else if (input === "/withdraw_funds") {
                const withdrawFundsText = document.createElement("div");
                withdrawFundsText.classList.add("line");
                withdrawFundsText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Funds withdrawn successfully to your main wallet!</span>`;
                outputDiv.appendChild(withdrawFundsText);
            } else if (input === "help") {
                const helpText = document.createElement("div");
                helpText.classList.add("line");
                helpText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Available commands: <b>/create_wallets</b>, <b>/balances</b>, <b>/buy_token</b>, <b>/import_wallet</b>, <b>/transfer_funds &lt;address&gt;</b>, <b>/withdraw_funds</b></span>`;
                outputDiv.appendChild(helpText);
            } else if (input === "clear") {
                document.querySelector(".output").innerHTML = '';
            } else {
                const unknownCommand = document.createElement("div");
                unknownCommand.classList.add("line");
                unknownCommand.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Unknown command: ${input}</span>`;
                outputDiv.appendChild(unknownCommand);
            }

            this.value = "";
            outputDiv.scrollTop = outputDiv.scrollHeight; // Auto-scroll to bottom
        }
    }
});
