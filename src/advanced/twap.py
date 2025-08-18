# src/advanced/twap.py

import os
import logging
import argparse
import time
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
logging.info("Script started: twap.py. Client initialized successfully.")

# --- Core TWAP Logic (Upgraded) ---
def execute_twap_order(symbol, side, total_quantity, duration_minutes, interval_seconds):
    """
    Executes a TWAP (Time-Weighted Average Price) order with a configurable interval.
    """
    try:
        # 1. Input Validation
        total_quantity = float(total_quantity)
        duration_minutes = int(duration_minutes)
        interval_seconds = int(interval_seconds)
        
        if total_quantity <= 0 or duration_minutes <= 0 or interval_seconds <= 0:
            error_msg = "Total quantity, duration, and interval must be positive."
            logging.error(error_msg)
            print(f"Error: {error_msg}")
            return

        # 2. Calculate order chunks based on the new interval
        total_duration_seconds = duration_minutes * 60
        if total_duration_seconds < interval_seconds:
            error_msg = "Total duration cannot be less than the interval."
            logging.error(error_msg)
            print(f"Error: {error_msg}")
            return
            
        num_chunks = total_duration_seconds // interval_seconds
        chunk_quantity = total_quantity / num_chunks
        
        # Fetch symbol precision rules and round the chunk quantity
        info = client.futures_exchange_info()
        symbol_info = next((s for s in info['symbols'] if s['symbol'] == symbol), None)
        if not symbol_info:
            raise ValueError(f"Invalid symbol: {symbol}")
        quantity_precision = symbol_info['quantityPrecision']
        chunk_quantity = round(chunk_quantity, quantity_precision)

        if chunk_quantity == 0:
             error_msg = "Total quantity is too small to be split over the given duration and interval."
             logging.error(error_msg)
             print(f"Error: {error_msg}")
             return

        logging.info(f"Starting TWAP {side.upper()} order for {total_quantity} {symbol} over {duration_minutes} minutes.")
        print(f"--- Starting TWAP Execution ---")
        print(f"Total Quantity: {total_quantity} {symbol}")
        print(f"Total Duration: {duration_minutes} minutes")
        print(f"Executing {num_chunks} orders of {chunk_quantity} {symbol} every {interval_seconds} seconds.")
        print("-----------------------------")

        # 3. The Execution Loop
        for i in range(num_chunks):
            try:
                logging.info(f"TWAP Chunk {i+1}/{num_chunks}: Placing market order for {chunk_quantity} {symbol}.")
                print(f"Executing chunk {i+1} of {num_chunks}...")
                
                client.futures_create_order(
                    symbol=symbol,
                    side=side.upper(),
                    type='MARKET',
                    quantity=chunk_quantity
                )
                
                print(f"Successfully placed market order for {chunk_quantity} {symbol}.")
                
                if i < num_chunks - 1:
                    print(f"Waiting {interval_seconds} seconds for next chunk...")
                    time.sleep(interval_seconds)

            except Exception as e:
                logging.error(f"ERROR in TWAP chunk {i+1}/{num_chunks}: {e}")
                print(f"An error occurred during chunk {i+1}: {e}. Continuing with next chunk.")
        
        logging.info("TWAP execution completed successfully.")
        print("\n--- TWAP Execution Complete ---")

    except Exception as e:
        logging.error(f"FATAL ERROR during TWAP execution for {symbol}: {e}")
        print(f"A fatal error occurred: {e}")

# --- Command-Line Interface (Upgraded) ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute a TWAP order on Binance Futures Testnet.")
    
    parser.add_argument("symbol", help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("side", choices=["BUY", "SELL"], help="Order side: BUY or SELL")
    parser.add_argument("total_quantity", type=float, help="Total quantity to trade")
    parser.add_argument("duration_minutes", type=int, help="Total duration in minutes for the execution")
    # Here is the new, user-friendly argument
    parser.add_argument("interval_seconds", type=int, help="Interval in seconds between each order")

    args = parser.parse_args()
    execute_twap_order(args.symbol, args.side, args.total_quantity, args.duration_minutes, args.interval_seconds)