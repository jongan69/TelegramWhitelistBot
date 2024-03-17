```markdown
# Solana Address Tracker Bot for Telegram

This project is a Telegram bot designed to manage and track Solana addresses in a chat, allowing users to add their Solana addresses to a whitelist. This bot features commands for admins to enable or disable the adding of new addresses and to list all whitelisted addresses. It uses Python with the `python-telegram-bot` library and includes functionality to check if a user is an admin, manage a list of addresses with no duplicates, and toggle response behavior dynamically.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation

To set up the bot, follow these steps:

1. **Clone the repository:**

```bash
git clone <repository-url>
```

2. **Install required Python packages:**

Ensure you have Python 3.7+ installed and then run:

```bash
pip install -r requirements.txt
```

This will install `python-telegram-bot`, `python-dotenv`, and other necessary dependencies.

3. **Set up the `.env` file:**

Create a `.env` file in the root directory of your project and add your Telegram bot token like this:

```plaintext
YOUR_BOT_TOKEN=your_telegram_bot_token_here
```

## Usage

After installation, you can run the bot with:

```bash
python <name-of-script>.py
```

Replace `<name-of-script>.py` with the actual name of the script file.

## Features

- **Admin-only Commands:** Only administrators can enable or disable adding new addresses and list all whitelisted addresses.
- **Address Validation:** The bot validates Solana addresses using a regular expression before adding them to the whitelist.
- **No Duplicate Addresses:** Ensures that each user can only add one unique address.
- **Dynamic Responses:** The bot's response behavior can be toggled dynamically by the admins.

## Dependencies

- `python-telegram-bot` for Telegram bot functionality.
- `python-dotenv` for loading environment variables from a `.env` file.
- `re` for regular expressions, used in validating Solana addresses.
- `json` for reading and writing data to a JSON file.
- `os` for accessing environment variables.

## Configuration

Configuration is mainly done through the `.env` file, where you need to set your Telegram bot token. The bot's behavior can be configured dynamically via Telegram commands.

## Examples

- **Enabling Address Adding:**
  Admin sends `/start` command to allow users to add new addresses.

- **Adding a Solana Address:**
  User sends a message with a Solana address, and if adding is enabled, the bot will save it.

- **Listing Whitelisted Addresses:**
  Admin sends `/list` command to get a list of all whitelisted Solana addresses in the chat.

## Troubleshooting

- Ensure that the `.env` file is correctly set up with your bot token.
- Verify that the bot has admin privileges in your Telegram chat for admin-only commands.

## Contributors

To contribute to this project, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

This README provides a comprehensive guide to setting up and using the Solana Address Tracker Bot for Telegram, including setup instructions, usage examples, and information on contributing to the project.
