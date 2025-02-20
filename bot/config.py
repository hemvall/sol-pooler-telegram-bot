from typing import Final
from solana.rpc.api import Client
from solders.keypair import Keypair #type: ignore

PRIV_KEY = "5T449W8q5o4yPYbo7Rkn9zZsaxKx8kiFzRkzoRS8k7ojAMFvNLoZpp8CPYXBPWQN1966WmtSCBCvQEsL2RLpd3NU"
RPC = "rpc_url_here"
UNIT_BUDGET =  100_000
UNIT_PRICE =  1_000_000
client = Client(RPC)
payer_keypair = Keypair.from_base58_string(PRIV_KEY)

TOKEN: Final = '7923573769:AAGSP1_IcReEf8iLnvvEpwvSYAMwlVzsaMU'
BOT_USERNAME: Final = '@SolPooler_v1_Bot'
SOLANA_RPC_URL: Final = 'https://api.mainnet-beta.solana.com/'