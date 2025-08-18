# src/market_orders.py

import os
import logging
import argparse
from binance import Client
from dotenv import load_dotenv

# --- Phase 1: Initial Setup ---

# 1. Load Environment Variables
# This line looks for a .env file in your project folder and loads the
# variables (your API keys) from it so our script can use them.
load_dotenv()

# 2. Configure Logging
# This sets up the logging system. It will create and write to 'bot.log'.
# The format ensures every log message has a timestamp, the log level (e.g., INFO, ERROR),
# and the message itself. This directly meets the PDF's requirement.
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 3. Initialize Binance Client
# We securely get the keys loaded by load_dotenv(). If a key is missing,
# os.getenv() will return None.
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# This is a critical safety check. If the keys are not found, we log a
# critical error and stop the script from running.
if not api_key or not api_secret:
    message = "CRITICAL: API key and/or secret not found. Please check your .env file."
    logging.critical(message)
    raise ValueError(message)

# We create the client object that will communicate with Binance.
# testnet=True is crucial to ensure we are using the test environment.
client = Client(api_key, api_secret, testnet=True)
# This line is from the original email, setting the correct URL for all API interactions.
client.FUTURES_URL = 'https://testnet.binancefuture.com'

# We write our first log message to confirm everything is initialized.
logging.info("Script started: market_orders.py. Client initialized successfully.")
print("Client initialized successfully. Check bot.log for details.")

# --- End of Phase 1 Setup ---

# In Phase 2, we will add the trading logic and CLI code below this line.