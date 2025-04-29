from ib_insync import IB
from strategies.defensive_strategy import evaluate_signal_from_df
from datetime import datetime
import pandas as pd
import yfinance as yf
import csv
import os
from pathlib import Path

today = datetime.today().strftime("%m/%d/%Y")

# Define root directory explicitly
ROOT_DIR = Path.cwd()
LOGS_DIR = ROOT_DIR / "logs"
TRADES_PATH = LOGS_DIR / "trades_shadow.csv"

# Ensure logs directory exists
LOGS_DIR.mkdir(exist_ok=True)

# === Constants ===
WATCHLIST = ['QQQM', 'VOO', 'IAU', 'IEFA', 'VWO', 'BOTZ', 'ROBO', 'XLE', 'VGK', 'EWJ', 'IJH', 'XLV', 'XLU']
# TRADES_PATH = 'logs/trades_shadow.csv'

# === Connect to IBKR (to read positions only) ===
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=101)

# === Wait for connection and fetch account ID ===
ib.sleep(1)
account_id = ib.managedAccounts()[0]  # uses the first available account

def log_shadow_trade(ticker, action, price, reason):
    file_exists = TRADES_PATH.exists()
    with open(TRADES_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'ticker', 'action', 'price', 'reason'])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ticker,
            action,
            round(price, 2),
            reason
        ])

# === Pull actual holdings (so we only "SELL" if we own) ===
portfolio = ib.positions()
held_positions = {p.contract.symbol: p.position for p in portfolio if p.position > 0}

# === Retrieve real-time account values
ib.sleep(1)
account_values = ib.accountValues()

# Safely find the NetLiquidation value
cash_available = None
for val in account_values:
    if val.tag == 'NetLiquidation' and val.currency == 'USD':
        cash_available = float(val.value)
        break

if cash_available is None:
    print("❌ Could not find NetLiquidation value in account values.")
    ib.disconnect()
    exit(1)

capital = cash_available
print(f"💰 Account value loaded: ${capital:,.2f}")

# === Main Loop: YF-only evaluation ===
for symbol in WATCHLIST:
    print(f"\n→ Evaluating {symbol} using yfinance...")

    try:
        # Pull full historical window for indicators
        yf_data = yf.download(symbol, period="100d", interval="1d", auto_adjust=False)
        if yf_data.empty:
            raise Exception("No data returned by yfinance")

        # Make sure columns are properly named
        df = yf_data[['Close', 'High', 'Low', 'Volume']].copy()
        print(f"[{symbol}] ✅ Retrieved {df.shape[0]} rows of data")

    except Exception as e:
        print(f"[{symbol}] ❌ Failed to fetch data: {e}")
        continue

    # === Evaluate Buy/Sell Logic ===
    buy, sell, price = evaluate_signal_from_df(df)

    if price is None:
        print(f"[{symbol}] ❎ Skipped — not enough data for signal")
        continue
    
    position_pct = 0.2
    max_pct_per_ticker = 0.4  # e.g. 40% of capital max in one asset

    # If already held, compute % of portfolio
    current_shares = held_positions.get(symbol, 0)
    current_value = current_shares * price
    if current_value / capital > max_pct_per_ticker:
        print(f"[{symbol}] ⚠️ Skipping BUY — position too large (${current_value:.2f} = {100 * current_value / capital:.1f}% of account)")
        continue
    
    max_trade_amt = capital * position_pct
    shares_to_trade = int(max_trade_amt / price)
    print(f"[{symbol}] ↳ Would trade {shares_to_trade} shares (~${max_trade_amt:.2f})") 
    
    if buy:
        print(f"[{symbol}] 🟢 Shadow BUY @ ${price:.2f} (yfinance)")
        log_shadow_trade(symbol, "BUY", price, "Signal from yfinance")
    elif sell:
        if held_positions.get(symbol, 0) > 0:
            print(f"[{symbol}] 🔴 Shadow SELL @ ${price:.2f} (yfinance)")
            log_shadow_trade(symbol, "SELL", price, "Signal from yfinance")
        else:
            print(f"[{symbol}] ⚪ Ignoring SELL — not held (yfinance)")
    else:
        print(f"[{symbol}] ⏸ HOLD — no signal (yfinance)")

print(f"{"="*10}End of Recs for {today}{"="*10}\n")


ib.disconnect()