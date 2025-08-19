# Binance Futures Trading Bot

This is a command-line interface (CLI) trading bot created for a Junior Python Developer assignment. The bot interacts with the Binance Futures Testnet to place market, limit, OCO, and TWAP orders.

---

## Features Implemented

* **Core Orders**: Fully functional scripts for placing **Market** and **Limit** orders.
* **Advanced Orders**:
    * **OCO (One-Cancels-the-Other)**: A script to open a position and immediately protect it with a linked take-profit and stop-loss order.
    * **TWAP (Time-Weighted Average Price)**: An algorithmic script to execute a large order over a user-defined period by breaking it into smaller chunks.
* **Secure API Handling**: API keys are managed securely using a `.env` file, which is ignored by Git.
* **Robust Logging**: All actions, successful orders, and API errors are logged with timestamps to `bot.log`.
* **Input Validation**: Each script includes checks for user input and pre-execution checks for exchange rules (e.g., minimum notional value for TWAP orders).

---

## Project Setup

### 1. Prerequisites
* Python 3.8+
* A Binance Futures Testnet account.

### 2. Clone the Repository
First, clone the project from GitHub. 
git clone [https://github.com/shivammpal/shivamkumar-binance-bot]
cd shivakumar-binance-bot

### 3. Install Dependencies
Install the necessary Python packages using pip.
pip install python-binance python-dotenv

### 4.Configure API Keys
Create a file named .env in the main project folder. Generate a new API Key and Secret from the Binance Futures Testnet website (from the "API Key" link in the footer) and add them to the file like this:

BINANCE_API_KEY="YOUR_API_KEY_HERE"
BINANCE_API_SECRET="YOUR_SECRET_KEY_HERE"

### How to Use the Bot
All commands must be run from the root directory of the project.

Market Order
To BUY 0.001 BTCUSDT at the current market price:

python src/market_orders.py BTCUSDT BUY 0.001
Limit Order
To place a limit order to SELL 0.01 ETHUSDT if the price reaches $4000:

python src/limit_orders.py ETHUSDT SELL 0.01 4000
OCO (Advanced)
To open a BUY position for 0.001 BTCUSDT and protect it with a take-profit at $70000 and a stop-loss at $68000:

python src/advanced/oco.py BTCUSDT BUY 0.001 70000 68000
TWAP (Advanced)
To BUY a total of 0.5 ETHUSDT over 5 minutes, placing one small order every 30 seconds:

python src/advanced/twap.py ETHUSDT BUY 0.5 5 30