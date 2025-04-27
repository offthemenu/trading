from ib_insync import IB, Stock, LimitOrder
from strategies.defensive_strategy import evaluate_signal_from_df
from datetime import datetime
import pandas as pd
import csv
import os
from pathlib import Path
import time

# === Settings ===
WATCHLIST = ['QQQM', 'VOO', 'IAU', 'IEFA', 'MCHI', 'BOTZ', 'ROBO', 'FCG', 'XOP', 'VGK', 'EWJ']
POSITION_PCT = 0.2
MAX_POSITION_PCT = 0.4
LIVE_MODE = True   # Toggle live trading on/off
today = datetime.today().strftime("%m/%d/%Y")

# === File + Log Paths ===
ROOT_DIR = Path.cwd()
LOGS_DIR = ROOT_DIR / "logs"
TRADES_PATH = LOGS_DIR / "trades_live_PROD_ibkr.csv"
LOGS_DIR.mkdir(exist_ok=True)

# === IBKR Setup ===
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=103, timeout=10)  # Different clientId for live executor
time.sleep(1)
account_id = ib.managedAccounts()[0]

# === Logging Function ===
def log_live_trade(ticker, action, price, shares, reason):
    file_exists = TRADES_PATH.exists()
    with open(TRADES_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'ticker', 'action', 'price', 'shares', 'reason'])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ticker,
            action,
            round(price, 2),
            shares,
            reason
        ])
# Logs number of shares per trade

# === Portfolio and Cash Check ===
portfolio = ib.positions()
held_positions = {p.contract.symbol: p.position for p in portfolio if p.position > 0}

account_values = ib.accountValues()
cash_available = None
for val in account_values:
    if val.tag == 'NetLiquidation' and val.currency == 'USD':
        cash_available = float(val.value)
        break

if cash_available is None:
    print("❌ Could not find NetLiquidation value.")
    ib.disconnect()
    exit(1)

capital = cash_available
print(f"💰 Account value: ${capital:,.2f}")

# === Main Loop ===
for symbol in WATCHLIST:
    print(f"\n→ Evaluating {symbol}...")

    try:
        contract = Stock(symbol, 'SMART', 'USD')
        ib.qualifyContracts(contract)

        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='100 D',
            barSizeSetting='1 day',
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1
        )

        if not bars:
            raise ValueError("No historical data returned.")

        df = pd.DataFrame(bars)
        df.rename(columns={'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume'}, inplace=True)

    except Exception as e:
        print(f"[{symbol}] ❌ Failed to fetch historical data: {e}")
        continue

    buy, sell, signal_price = evaluate_signal_from_df(df)
    if signal_price is None:
        print(f"[{symbol}] ❎ Skipped — not enough data for signal")
        continue

    snapshot = ib.reqMktData(contract, "", False, False)
    time.sleep(1)

    execution_price = None
    if snapshot.bid and snapshot.ask and snapshot.bid > 0 and snapshot.ask > 0:
        execution_price = (snapshot.bid + snapshot.ask) / 2
    elif snapshot.last and snapshot.last > 0:
        execution_price = snapshot.last
    elif signal_price:
        execution_price = signal_price

    if not execution_price or pd.isna(execution_price):
        print(f"[{symbol}] ❌ No execution price, skipping.")
        continue

    current_shares = held_positions.get(symbol, 0)
    current_value = current_shares * execution_price

    if current_value / capital > MAX_POSITION_PCT:
        print(f"[{symbol}] ⚠️ Position too large ({current_value/capital:.1%}), skipping BUY.")
        continue

    shares_to_trade = int((capital * POSITION_PCT) / execution_price)
    if shares_to_trade == 0:
        print(f"[{symbol}] ⚠️ Trade size too small, skipping.")
        continue

    if buy:
        print(f"[{symbol}] 🟢 BUY signal detected @ ${execution_price:.2f}")

        if LIVE_MODE:
            order = LimitOrder('BUY', shares_to_trade, round(execution_price, 2))
            trade = ib.placeOrder(contract, order)
            print(f"[{symbol}] 🚀 Placed LIMIT BUY for {shares_to_trade} shares at ${execution_price:.2f}")
        else:
            print(f"[{symbol}] 🧪 Dry-Run: Would BUY {shares_to_trade} shares at ${execution_price:.2f}")

        log_live_trade(symbol, "BUY", execution_price, shares_to_trade, "Live Signal")

    elif sell:
        if current_shares > 0:
            print(f"[{symbol}] 🔴 SELL signal detected @ ${execution_price:.2f}")

            if LIVE_MODE:
                order = LimitOrder('SELL', current_shares, round(execution_price, 2))
                trade = ib.placeOrder(contract, order)
                print(f"[{symbol}] 🚀 Placed LIMIT SELL for {current_shares} shares at ${execution_price:.2f}")
            else:
                print(f"[{symbol}] 🧪 Dry-Run: Would SELL {current_shares} shares at ${execution_price:.2f}")

            log_live_trade(symbol, "SELL", execution_price, current_shares, "Live Signal")
        else:
            print(f"[{symbol}] ⚪ Ignored SELL — no position held.")

    else:
        print(f"[{symbol}] ⏸ HOLD — no action.")

# === End of Run ===
print(f"{'='*10} End of Execution {today} {'='*10}")
ib.disconnect()  # 🆕 NEW: Always disconnect at the end