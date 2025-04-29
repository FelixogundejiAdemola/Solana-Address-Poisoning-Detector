# Solana Address Poisoning Detector

This Python script detects suspicious activities related to **address poisoning attacks** on the Solana blockchain.  
It analyzes the transaction history of your wallet, identifies addresses that send tiny amounts (dust) or mimic your real contacts, and saves suspicious addresses into a text file.

---

## 📜 What is Address Poisoning?
- Attackers send small ("dust") transactions to your wallet.
- They create wallet addresses that **look similar** to real ones you trust.
- If you're not careful when copying/pasting addresses, you might send funds to the attacker's address instead of the correct one.
- This script **analyzes** and **flags** such suspicious addresses.

---

## 🔧 How It Works
1. Fetch your latest 100 transaction signatures.
2. For each transaction:
   - Look for **small transfers** (less than or equal to 0.0001 SOL).
   - Record senders and recipients.
3. Compare:
   - If an incoming address **matches the first 3 characters** of an outgoing address, it is marked as a **poison** attempt.
   - Otherwise, it is flagged as **dust**.
4. Save results into a text file (`suspicious_addresses.txt`).

---

## 🚀 How To Use

### 1. Clone this repository
```bash
git clone https://github.com/yourname/solana-address-poisoning-detector.git
cd solana-address-poisoning-detector
```

### 2. Install Requirements
```bash
pip install requests python-dotenv
```

### 3. Set up `.env` file
Create a `.env` file in the project folder and add:

```bash
HELIUS_API_KEY=your_helius_api_key_here
YOUR_SOL_WALLET_ADDRESS=your_wallet_address_here
```

> ⚡ You can get a free Helius API key from [https://helius.dev/](https://helius.dev/).

### 4. Run the script
```bash
python main.py
```

---

## 📂 Output
- A file named `suspicious_addresses.txt` will be created.
- It lists suspicious addresses in the format:

```
<attacker_address> : poison
<dust_address> : dust
```

- `poison` = likely trying to confuse you.
- `dust` = random small transfer, not mimicking your address.

---

## 📋 Notes
- Only **System Program** (`program: "system"`) transfer transactions are analyzed.
- A small delay (`2.5 seconds`) between transactions prevents hitting API rate limits.
- This script is read-only: it **does not perform** any wallet operations.

---

## 📖 Example

**Terminal output:**
```
[*] Fetching transaction signatures...
[*] Found 100 signatures. Fetching transaction details...
[*] Fetching transaction for signature: 5bPz...
[*] Transaction details fetched for signature: 5bPz...
...
[*] Comparing suspicious addresses...
[✓] Results saved to suspicious_addresses.txt
```

---

## 👨‍💻 Author
- Built by [YourNameHere]
