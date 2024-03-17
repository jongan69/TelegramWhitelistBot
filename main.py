import os
import re
import json
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()  # Take environment variables from .env.

YOUR_BOT_TOKEN = os.environ.get("YOUR_BOT_TOKEN")

# Regular expression for detecting Solana addresses.
SOLANA_ADDRESS_PATTERN = r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b"

def read_addresses():
    """Read the addresses from the JSON file."""
    try:
        with open("solana_addresses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_address(address):
    """Save the detected Solana address to a JSON file, ensuring no duplicates."""
    addresses = read_addresses()
    if address not in addresses:  # Check if the address is not already in the list
        addresses.append(address)
        with open("solana_addresses.json", "w") as file:
            json.dump(addresses, file, indent=4)
            return True  # Indicate that the address was new and saved
    return False  # Indicate that the address was a duplicate and not saved

async def message_handler(update, context):
    """Check every message for Solana addresses and ensure no duplicates are saved."""
    message_text = update.message.text
    solana_matches = re.findall(SOLANA_ADDRESS_PATTERN, message_text)
    if solana_matches:
        for address in solana_matches:
            if save_address(address):  # Only reply if the address was new and saved
                await update.message.reply_text(f"Saved Solana address: {address}")
            else:
                await update.message.reply_text("This Solana address is already saved.")
    else:
        await update.message.reply_text("Please provide a valid Solana address. This whitelist only accepts Solana addresses.")

def main():
    token = YOUR_BOT_TOKEN
    application = Application.builder().token(token).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("Telegram Bot started with Solana address whitelist and no duplicates!", flush=True)
    application.run_polling()

if __name__ == '__main__':
    main()
