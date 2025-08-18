# src/limit_orders.py

import os
import logging
import argparse
from binance import Client
from dotenv import load_dotenv

# --- Phase 1: Initial Setup (Same as before) ---
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
logging.info("Script started: limit_orders.py. Client initialized successfully.")

# --- Phase 2: Core Logic and CLI ---

def place_limit_order(symbol, side, quantity, price):
    """Places a limit order on Binance Futures."""
    try:
        # Input Validation for both quantity and price
        quantity = float(quantity)
        price = float(price)
        if quantity <= 0 or price <= 0:
            error_msg = f"Invalid quantity or price. Quantity: {quantity}, Price: {price}. Both must be positive."
            logging.error(error_msg)
            print(f"Error: {error_msg}")
            return None

        logging.info(f"Attempting to place LIMIT {side.upper()} order for {quantity} {symbol} at price {price}...")
        print(f"Placing LIMIT {side.upper()} order for {quantity} {symbol} at price {price}...")

        # The API call now includes 'type', 'price', and 'timeInForce'
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type=Client.ORDER_TYPE_LIMIT,
            timeInForce=Client.TIME_IN_FORCE_GTC, # Good 'Til Canceled
            quantity=quantity,
            price=price
        )

        logging.info(f"SUCCESS: Limit order placed. Response: {order}")
        print("Successfully placed limit order!")
        print(f"--- Order ID: {order['orderId']}, Symbol: {order['symbol']}, Price: {order['price']}, Quantity: {order['origQty']} ---")
        return order

    except Exception as e:
        logging.error(f"ERROR placing limit order for {symbol}: {e}")
        print(f"An error occurred: {e}")
        return None

# --- Command-Line Interface (CLI) ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Place a limit order on Binance Futures Testnet.")

    # We add the new 'price' argument
    parser.add_argument("symbol", help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("side", choices=["BUY", "SELL"], help="Order side: BUY or SELL")
    parser.add_argument("quantity", type=float, help="Order quantity (e.g., 0.01)")
    parser.add_argument("price", type=float, help="Price at which to place the order")

    args = parser.parse_args()
    place_limit_order(args.symbol, args.side, args.quantity, args.price)