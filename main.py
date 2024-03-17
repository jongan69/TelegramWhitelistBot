import os
import re
import json
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()  # Take environment variables from .env.

YOUR_BOT_TOKEN = os.environ.get("YOUR_BOT_TOKEN")

# Regular expression for detecting Solana addresses.
SOLANA_ADDRESS_PATTERN = r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b"

def read_addresses():
    """Read the addresses from the JSON file."""
    try:
        with open("solana_addresses_by_chat.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_address(chat_id, address):
    """Save the detected Solana address to a JSON file by chat ID, ensuring no duplicates."""
    addresses = read_addresses()
    if chat_id not in addresses:
        addresses[chat_id] = []
    if address not in addresses[chat_id]:  # Check if the address is not already in the list for this chat
        addresses[chat_id].append(address)
        with open("solana_addresses_by_chat.json", "w") as file:
            json.dump(addresses, file, indent=4)
            return True  # Indicate that the address was new and saved
    return False  # Indicate that the address was a duplicate and not saved

async def message_handler(update, context: ContextTypes.DEFAULT_TYPE):
    """Check every message for Solana addresses and ensure no duplicates are saved, managing a separate list for each chat."""
    chat_type = update.message.chat.type
    if chat_type != "private":
        chat_id = str(update.message.chat.id)
        message_text = update.message.text
        
        solana_matches = re.findall(SOLANA_ADDRESS_PATTERN, message_text)
        if solana_matches:
            for address in solana_matches:
                if save_address(chat_id, address):  # Only reply if the address was new and saved
                    await update.message.reply_text(f"Saved Solana address: {address}")
                else:
                    await update.message.reply_text("This Solana address is already saved in this chat.")
        else:
            await update.message.reply_text("Please provide a valid Solana address. This whitelist only accepts Solana addresses.")
    else:
        await update.message.reply_text("Please add me to a group or channel to manage Solana addresses for everyone you lilShid")

async def list_addresses(update, context: ContextTypes.DEFAULT_TYPE):
    """List all whitelisted Solana addresses for the chat, in chunks if necessary."""
    chat_id = str(update.message.chat.id)
    addresses = read_addresses()
    if chat_id in addresses and addresses[chat_id]:
        # Prepare the initial part of the message.
        base_message = "Whitelisted Solana addresses:\n"
        current_message = base_message

        for address in addresses[chat_id]:
            # If adding another address exceeds the limit, send the current message and start a new one.
            if len(current_message) + len(address) + 1 > 4096:  # +1 for the newline character
                await update.message.reply_text(current_message)
                current_message = base_message  # Reset with the base message for continuity.
            current_message += address + "\n"
        
        # Send any remaining addresses in the final chunk.
        if current_message != base_message:
            await update.message.reply_text(current_message)
    else:
        await update.message.reply_text("No whitelisted Solana addresses found for this chat.")

def main():
    token = YOUR_BOT_TOKEN
    application = Application.builder().token(token).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_handler(CommandHandler("list", list_addresses))  # Register the /list command handler
    print("Telegram Bot started with channel-specific Solana address whitelist and no duplicates!", flush=True)
    application.run_polling()

if __name__ == '__main__':
    main()
