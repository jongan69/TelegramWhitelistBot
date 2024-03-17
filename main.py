import os
import re
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import itertools

load_dotenv()  # Take environment variables from .env.
YOUR_BOT_TOKEN = os.environ.get("YOUR_BOT_TOKEN")
SOLANA_ADDRESS_PATTERN = r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b"

toggle = itertools.cycle([True, False]).__next__
YAP = False

async def is_user_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if the user is an admin of the chat."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # For private chats, the user is considered an admin.
    if update.effective_chat.type == "private":
        return True

    # Check admin status in non-private chats.
    admins = await context.bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admins)

async def start_adding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Allow adding of new addresses if the user is an admin."""
    if not await is_user_admin(update, context):
        if YAP:
            await update.message.reply_text("This command can only be used by administrators.")
        return
    
    chat_id = str(update.message.chat.id)
    addresses = read_addresses()
    if chat_id not in addresses:
        addresses[chat_id] = {"adding_allowed": False, "addresses": {}}
    addresses[chat_id]['adding_allowed'] = True
    write_addresses(addresses)
    if YAP:
        await update.message.reply_text("Adding new Solana addresses is now allowed.")

async def stop_adding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop adding of new addresses if the user is an admin."""
    if not await is_user_admin(update, context):
        if YAP:
            await update.message.reply_text("This command can only be used by administrators.")
        return
    
    chat_id = str(update.message.chat.id)
    addresses = read_addresses()
    if chat_id not in addresses:
        addresses[chat_id] = {"adding_allowed": False, "addresses": {}}
    addresses[chat_id]['adding_allowed'] = False
    write_addresses(addresses)
    if YAP:
        await update.message.reply_text("Adding new Solana addresses is now disabled.")

async def message_handler(update, context: ContextTypes.DEFAULT_TYPE):
    """Check every message for Solana addresses and ensure no duplicates are saved, managing a separate list for each chat."""
    chat_id = str(update.message.chat.id)
    user_id = str(update.effective_user.id)
    message_text = update.message.text
    
    addresses = read_addresses()
    if chat_id not in addresses or not addresses[chat_id].get('adding_allowed', False):
        if YAP:
            await update.message.reply_text("Adding new Solana addresses is currently not allowed in this chat.")
        return

    solana_matches = re.findall(SOLANA_ADDRESS_PATTERN, message_text)
    if solana_matches:
        for address in solana_matches:
            if user_id not in addresses[chat_id]["addresses"]:
                addresses[chat_id]["addresses"][user_id] = address
                write_addresses(addresses)
                await update.message.reply_text(f"Saved Solana address: {address}")
            else:
                if YAP:
                    await update.message.reply_text("Each user can only save one address.")
    else:
        if YAP:
            await update.message.reply_text("Please provide a valid Solana address. This whitelist only accepts Solana addresses.")

def read_addresses():
    """Read the addresses from the JSON file."""
    try:
        with open("solana_addresses_by_chat.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_addresses(addresses):
    """Write the addresses to the JSON file."""
    with open("solana_addresses_by_chat.json", "w") as file:
        json.dump(addresses, file, indent=4)
        
async def list_addresses(update, context: ContextTypes.DEFAULT_TYPE):
    """List all whitelisted Solana addresses for the chat, in chunks if necessary."""
    chat_id = str(update.message.chat.id)
    addresses = read_addresses()
    if chat_id in addresses and addresses[chat_id]:
        # Prepare the initial part of the message.
        base_message = "Whitelisted Solana addresses:\n"
        current_message = base_message
        all_addresses = addresses[chat_id]["addresses"]

        for user in all_addresses:
            address = all_addresses[user]
            print(f"User {user} has wallet {address}")
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
        
async def toggleYap(update, context: ContextTypes.DEFAULT_TYPE):
    global YAP  # Declare the variable as global to modify it
    if not await is_user_admin(update, context):
        if YAP:
            await update.message.reply_text("This command can only be used by administrators.")
        return
    YAP = toggle()
    await update.message.reply_text(f"Yapp is set to {YAP}")
    return YAP
    
def main():
    
    application = Application.builder().token(YOUR_BOT_TOKEN).build()
    application.add_handler(CommandHandler("yap", toggleYap))
    application.add_handler(CommandHandler("start", start_adding))
    application.add_handler(CommandHandler("stop", stop_adding))
    application.add_handler(CommandHandler("list", list_addresses))  # Register the /list command handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot started with enhanced functionality!", flush=True)
    application.run_polling()

if __name__ == '__main__':
    main()
