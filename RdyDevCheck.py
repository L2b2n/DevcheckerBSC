import requests
from prettytable import PrettyTable
import json
import pandas as pd

# API URLs and API keys
bsc_api_key = "VCBK77BR9GDMXKJDQ36MVYW9KYEWG6EW9H"
api_url_latest_block = "https://api.bscscan.com/api?module=proxy&action=eth_getBlockByNumber&tag=latest&boolean=true"

# Connect to the Binance Smart Chain network

# Address of the deployment wallet to be checked
deploy_wallet_address = "0xC5824Df4086012a3C917a074d21412a3e6D95403"

# Initialize the table
table = PrettyTable()
table.field_names = ["Type", "Link"]

# Check transactions for the deployment wallet
api_url = f"https://api.bscscan.com/api?module=account&action=txlist&address={deploy_wallet_address}&apikey={bsc_api_key}"
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    transactions = data["result"]
    print(f"Number of transactions for the deployment wallet: {len(transactions)}")
    # Check for new contracts and token transfers
    deploy_contracts = 0
    for transaction in transactions:
        input_data = transaction["input"]
        if (
            "getcontractcreation" in input_data
            or "0x60806040" in input_data
            or "0x620493e0" in input_data
        ):
            deploy_contracts += 1
            table.add_row(
                [
                    "New Contract Deployed",
                    f"https://bscscan.com/tx/{transaction['hash']}",
                ]
            )
    print(f"Number of new contracts deployed: {deploy_contracts}")
# Check for token swaps and transfers
token_swaps = 0
token_transfers = 0
for transaction in transactions:
    input_data = transaction["input"]
    if "getcontractcreation" in input_data or "0xfb3bdb41" in input_data:
        token_swaps += 1
        table.add_row(["Token Swap", f"https://bscscan.com/tx/{transaction['hash']}"])
    elif "0xa9059cbb" in input_data:
        token_transfers += 1
        table.add_row(["Token Transfer", f"https://bscscan.com/tx/{transaction['hash']}"])

print(f"Number of Tokenswaps: {token_swaps}")
print(f"Number of Token Transfers: {token_transfers}")
    # Check for airdrops
airdrops = 0
for transaction in transactions:
    input_data = transaction["input"]
    if "getcontractcreation" in input_data or input_data.startswith("0xa9059cbb"):
        airdrops += 1
        table.add_row(["Airdrop", f"https://bscscan.com/tx/{transaction['hash']}"])
print(f"Number of Airdrops: {airdrops}")
    


print(table)
