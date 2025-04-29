import requests
import os
from dotenv import load_dotenv
import time


# Load environment variables

load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
USER_ADDRESS = os.getenv("YOUR_SOL_WALLET_ADDRESS")
RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"

headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

received_from = set()
sent_to = set()
suspicious = {}
def get_signatures(address, limit=100): # You can adjust the limit as needed
    """Fetch signatures for transactions involving the address."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [address, {"limit": limit}]
    }
    try:
        response = requests.post(RPC_URL, json=payload, headers=headers)
        response.raise_for_status()
        return [sig["signature"] for sig in response.json().get("result", [])]
    except requests.RequestException as e:
        print(f"[!] Error fetching signatures: {e}")
        return []
   

def get_transactions(signature):
    """Fetch parsed transactions for a list of signatures."""
    payload = {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getTransaction",
  "params": [
    signature,
    {
     "encoding": "jsonParsed"
    }
  ]
        }
    try:
        response = requests.post(RPC_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("result", {})
    except requests.RequestException as e:
        print(f"[!] Error fetching transaction {signature}: {e}")
        return {}

def analyze_transactions(user_address):
    """Analyze transactions to detect suspicious (potential poisoning) activity."""

    print("[*] Fetching transaction signatures...")
    signatures = get_signatures(user_address)
    if not signatures:
        print("[!] No transactions found.")
        return {}

    print(f"[*] Found {len(signatures)} signatures. Fetching transaction details...")
    for signature in signatures:
        print(f"[*] Fetching transaction for signature: {signature}")
        transaction = get_transactions(signature)
        if not transaction:
            print(f"[!] No transaction details found for signature: {signature}")
            continue
        print(f"[*] Transaction details fetched for signature: {signature}")
       

        instructions = transaction.get("transaction", {}).get("message", {}).get("instructions", [])
        for ix in instructions:
            if ix.get("program") != "system":
                continue    # Only analyze system program transfers

            parsed = ix.get("parsed", {})
            if parsed.get("type") == "transfer":
                info = parsed.get("info", {})
                source = info.get("source")
                destination = info.get("destination")
                lamports = int(info.get("lamports", 0))

                if destination == user_address and lamports <= 100_000:
                    received_from.add(source)

                if source == user_address:
                    sent_to.add(destination)
        time.sleep(2.5)  # Rate limit to avoid hitting API too hard
    print(received_from)
    print(sent_to)
    print("[*] Comparing suspicious addresses...")
    # Compare received_from and sent_to
    for spammer in received_from:
        matched = False
        for legit in sent_to:
            if spammer[:3] == legit[:3]:  # First 3 characters match
                suspicious[spammer] = 'poison'
                matched = True
                break  # Exit the loop once a match is found
        if not matched:
            suspicious[spammer] = 'dust'

    return suspicious

def save_to_txt(data, filename="suspicious_addresses.txt"):
    """Save the suspicious addresses to a text file."""
    with open(filename, "w") as f:
        if not data:
            f.write("No suspicious addresses found.\n")
            return
        for spammer, mimic in data.items():
            f.write(f"{spammer} : {mimic}\n")
    print(f"[✓] Results saved to {filename}")

if __name__ == "__main__":
    if not HELIUS_API_KEY or not USER_ADDRESS:
        print("Please set HELIUS_API_KEY and YOUR_SOLANA_ADDRESS in a .env file.")
    else:
        result = analyze_transactions(USER_ADDRESS)
        save_to_txt(result)
