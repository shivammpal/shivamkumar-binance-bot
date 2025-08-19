# src/advanced/sentiment_trader.py

import os
import logging
import argparse
import pandas as pd
from binance import Client
from dotenv import load_dotenv

# --- Standard Setup ---
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
logging.info("Script started: sentiment_trader.py. Client initialized successfully.")

# --- Core Sentiment Logic ---

def get_latest_fear_and_greed_index():
    """Reads the CSV file and returns the most recent index value."""
    try:
        # We assume the CSV file is in the root project directory
        df = pd.read_csv('fear_and_greed_index.csv')
        # The last row contains the most recent value
        latest_value = int(df.iloc[-1]['value'])
        logging.info(f"Successfully read Fear & Greed Index. Latest value: {latest_value}")
        return latest_value
    except FileNotFoundError:
        logging.error("ERROR: fear_and_greed_index.csv not found in project directory.")
        print("Error: Could not find 'fear_and_greed_index.csv'. Please download it and place it in the main project folder.")
        return None
    except Exception as e:
        logging.error(f"ERROR reading CSV file: {e}")
        print(f"An error occurred while reading the data file: {e}")
        return None

def execute_sentiment_trade(symbol, quantity):
    """Executes a trade based on the Fear & Greed Index."""
    print("--- Starting Smart Sentiment Trader ---")
    index_value = get_latest_fear_and_greed_index()

    if index_value is None:
        print("Could not retrieve sentiment data. Exiting.")
        return

    print(f"Current Fear & Greed Index: {index_value}")
    
    side = None
    # Define our trading logic thresholds
    EXTREME_FEAR_THRESHOLD = 25
    EXTREME_GREED_THRESHOLD = 75

    if index_value <= EXTREME_FEAR_THRESHOLD:
        print(f"Sentiment is 'Extreme Fear' ({index_value}). This is a potential buying opportunity.")
        side = 'BUY'
    elif index_value >= EXTREME_GREED_THRESHOLD:
        print(f"Sentiment is 'Extreme Greed' ({index_value}). This is a potential selling opportunity.")
        side = 'SELL'
    else:
        print(f"Sentiment is 'Neutral' ({index_value}). No action will be taken.")
        logging.info("Sentiment is neutral. No trade executed.")
        return

    try:
        print(f"Action: Placing MARKET {side} order for {quantity} {symbol}...")
        logging.info(f"Sentiment Trigger: Placing MARKET {side} order for {quantity} {symbol}...")
        
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        
        logging.info(f"SUCCESS: Sentiment-based order placed. Response: {order}")
        print("Successfully placed market order!")
        print(f"--- Order ID: {order['orderId']}, Symbol: {order['symbol']}, Quantity: {order['origQty']} ---")

    except Exception as e:
        logging.error(f"ERROR placing sentiment-based market order for {symbol}: {e}")
        print(f"An error occurred while placing the order: {e}")

# --- Command-Line Interface ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trade based on the Fear & Greed Index.")
    
    parser.add_argument("symbol", help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("quantity", type=float, help="Order quantity to use if a trade is triggered")

    args = parser.parse_args()
    execute_sentiment_trade(args.symbol, args.quantity)