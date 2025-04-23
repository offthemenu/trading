import csv
import os
from datetime import datetime

# Define file paths and initial capital for simulated trading

POSITIONS_PATH = 'logs/positions_live.csv'
TRADES_PATH = 'logs/trades_live.csv'
INITIAL_CAPITAL = 10000  # Starting simulated capital

def read_positions():
    '''
    Reads the current portfolio from the positions in the CSV File
    Returns a dict of {ticker: {'shares': x, 'avg_price': y}}
    '''
    
    positions = {}
    
    with open(POSITIONS_PATH, "r") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            ticker = row["ticker"]
            shares = float(row["shares"])
            avg_price = float(row["avg_price"])
            positions[ticker] = {"shares": shares, "avg_price": avg_price}
    
    return positions

def write_positions(positions):
    '''
    Writes the updated portfolio back to the positions CSV File.
    Overwrites the entire file with th enew values
    ''' 
    with open(POSITIONS_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ticker", "shares", "avg_price"])
        writer.writeheader()
        for ticker, data in positions.items():
            writer.writerow({"ticker": ticker, "shares": data["shares"], "avg_price": data["avg_price"]})

def log_trade(ticker, action, price, shares, reason):
    '''
    Appends a trade event (buy or sell) to the trades log file
    If the file doesn't exist, it creates headers
    '''
    
    file_exists = os.path.isfile(TRADES_PATH)
    with open(TRADES_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["date", "ticker", "action", "price", "shares", "reason"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ticker, action, price, shares, reason])
        
def calculate_portfolio_value(positions, prices):
    '''
    Calculates the total value of all held positions using current prices
    Returns total invested value
    '''
    value = 0
    for ticker, data in positions.items():
        value += data["shares"] * prices.get(ticker,0)
    return value
    
def get_cash_available(positions, prices):
    '''
    Calculates remaining cash avilable to trade
    Based on: initial capital - value of current positions
    '''
    invested = calculate_portfolio_value(positions, prices)
    return INITIAL_CAPITAL - invested