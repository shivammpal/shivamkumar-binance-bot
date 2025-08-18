# src/market_orders.py

import os
import logging
import argparse
from binance import Client
from dotenv import load_dotenv

# --- Phase 1: Initial Setup ---
load_dotenv()
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
if not api_key or not api_secret:
    message = "CRITICAL: API key and/or secret not found. Please check your .env file."
    logging.critical(message)
    raise ValueError(message)
client = Client(api_key, api_secret, testnet=True)
client.FUTURES_URL = 'https://testnet.binancefuture.com'
logging.info("Script started: market_orders.py. Client initialized successfully.")

# --- Phase 2: Core Logic and CLI ---

def place_market_order(symbol, side, quantity):
    """
    Places a market order on Binance Futures.
    This function contains the core trading logic.
    """
    try:
        # 1. Input Validation (as required by the PDF)
        # We convert quantity to a float and check if it's positive.
        quantity = float(quantity)
        if quantity <= 0:
            logging.error(f"Invalid quantity: {quantity}. Quantity must be positive.")
            print(f"Error: Invalid quantity '{quantity}'. Must be a positive number.")
            return None

        # 2. Log the attempt
        # This is good practice and meets the logging requirement.
        logging.info(f"Attempting to place MARKET {side.upper()} order for {quantity} {symbol}...")
        print(f"Placing MARKET {side.upper()} order for {quantity} {symbol}...")

        # 3. The API Call
        # This is the line that actually sends the order to Binance.
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )

        # 4. Log and print the success message
        logging.info(f"SUCCESS: Market order placed. Response: {order}")
        print("Successfully placed market order!")
        print(f"--- Order ID: {order['orderId']}, Symbol: {order['symbol']}, Quantity: {order['origQty']} ---")
        return order

    except Exception as e:
        # 5. Error Handling
        # If anything goes wrong in the 'try' block, this code will run.
        logging.error(f"ERROR placing market order for {symbol}: {e}")
        print(f"An error occurred: {e}")
        return None

# --- Command-Line Interface (CLI) ---
# This part of the script runs only when you execute it directly from the terminal.
if __name__ == "__main__":
    # 1. Create the parser
    # argparse is the standard Python library for creating CLIs.
    parser = argparse.ArgumentParser(description="Place a market order on Binance Futures Testnet.")

    # 2. Add the arguments the user needs to provide
    parser.add_argument("symbol", help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("side", choices=["BUY", "SELL"], help="Order side: BUY or SELL")
    parser.add_argument("quantity", type=float, help="Order quantity (e.g., 0.01)")

    # 3. Parse the arguments from the terminal
    args = parser.parse_args()

    # 4. Call our main function with the user's input
    place_market_order(args.symbol, args.side, args.quantity)