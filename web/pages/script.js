const commands = [
    "/create_wallets",
    "/balances",
    "/buy_token",
    "/import_wallet",
    "/transfer_funds",
    "/withdraw_funds"
];

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

function checkInputField(){
    
}
function aa(){

}

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
                const createWalletsText = document.createElement("div");
                createWalletsText.classList.add("line");
                createWalletsText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Wallets created successfully!</span>`;
                outputDiv.appendChild(createWalletsText);
            } else if (input === "/balances") {
                const balancesText = document.createElement("div");
                balancesText.classList.add("line");
                balancesText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Balances: SOL: 1000.00, USDT: 500.00</span>`;
                outputDiv.appendChild(balancesText);
            } else if (input === "/buy_token") {
                const buyTokenText = document.createElement("div");
                buyTokenText.classList.add("line");
                buyTokenText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Token purchased successfully!</span>`;
                outputDiv.appendChild(buyTokenText);
            } else if (input === "/import_wallet") {
                const importWalletText = document.createElement("div");
                importWalletText.classList.add("line");
                importWalletText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Wallet imported successfully!</span>`;
                outputDiv.appendChild(importWalletText);
            } else if (input.startsWith("/transfer_funds")) {
                const transferFundsText = document.createElement("div");
                transferFundsText.classList.add("line");
                const destination = input.split(" ")[1] || "No address provided";
                transferFundsText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Funds transferred to ${destination}.</span>`;
                outputDiv.appendChild(transferFundsText);
            } else if (input === "/withdraw_funds") {
                const withdrawFundsText = document.createElement("div");
                withdrawFundsText.classList.add("line");
                withdrawFundsText.innerHTML = `<span class="prompt">C:\\Users\\Spool&gt;</span> <span class="command">Funds withdrawn successfully!</span>`;
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
