from ib_insync import IB, Stock
from strategies.defensive_strategy import evaluate_signal_from_df
from datetime import datetime
import pandas as pd
import csv
import os
from pathlib import Path

today = datetime.today().strftime("%m/%d/%Y")

# === File + Log Paths ===
ROOT_DIR = Path(__file__).resolve().parent
LOGS_DIR = ROOT_DIR / "logs"
TRADES_PATH = LOGS_DIR / "trades_shadow_ibkr.csv"
LOGS_DIR.mkdir(exist_ok=True)

# === IBKR Setup ===
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=102, timeout=10)
ib.sleep(1)
account_id = ib.managedAccounts()[0]

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

# === Portfolio and Cash Check ===
portfolio = ib.positions()
held_positions = {p.contract.symbol: p.position for p in portfolio if p.position > 0}

ib.sleep(1)
account_values = ib.accountValues()
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

# === Ticker Set ===
WATCHLIST = ['QQQM', 'VOO', 'IAU', 'IEFA', 'MCHI', 'BOTZ', 'ROBO', 'FCG', 'XOP', 'VGK', 'EWJ']

# === Main Loop: IBKR market data (not yfinance) ===
for symbol in WATCHLIST:
    print(f"\n→ Evaluating {symbol} using IBKR snapshot data...")

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
            raise ValueError("No historical data returned")

        df = pd.DataFrame(bars)
        df.rename(columns={'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume'}, inplace=True)
        print(f"[{symbol}] ✅ Retrieved {df.shape[0]} rows of data from IBKR")

    except Exception as e:
        print(f"[{symbol}] ❌ Failed to fetch IBKR data: {e}")
        continue

    buy, sell, signal_price = evaluate_signal_from_df(df)
    if signal_price is None:
        print(f"[{symbol}] ❎ Skipped — not enough data for signal")
        continue
    
    # Fetch live quote
    snapshot = ib.reqMktData(contract, "", False, False)
    ib.sleep(1)

    # === Execution Price Resolution ===
    execution_price = None

    # Prefer bid/ask midpoint
    if snapshot.bid is not None and snapshot.ask is not None and snapshot.bid > 0 and snapshot.ask > 0:
        execution_price = (snapshot.bid + snapshot.ask) / 2
    elif snapshot.last is not None and snapshot.last > 0:
        execution_price = snapshot.last
    elif signal_price is not None and signal_price > 0:
        execution_price = signal_price  # Fallback to signal_close

    # Final check
    if execution_price is None or pd.isna(execution_price):
        print(f"[{symbol}] ❌ Still no execution price after fallback. Skipping.")
        continue

    position_pct = 0.2
    max_pct_per_ticker = 0.4

    current_shares = held_positions.get(symbol, 0)
    current_value = current_shares * execution_price

    if current_value / capital > max_pct_per_ticker:
        print(f"[{symbol}] ⚠️ Skipping BUY — position too large (${current_value:.2f} = {100 * current_value / capital:.1f}% of account)")
        continue

    shares_to_trade = int((capital * position_pct) / execution_price)
    print(f"[{symbol}] ↳ Would trade {shares_to_trade} shares at ${execution_price:.2f}")

    if buy:
        print(f"[{symbol}] 🟢 Shadow BUY @ ${execution_price:.2f} (IBKR)")
        log_shadow_trade(symbol, "BUY", execution_price, "Signal from IBKR")
    elif sell:
        if held_positions.get(symbol, 0) > 0:
            print(f"[{symbol}] 🔴 Shadow SELL @ ${execution_price:.2f} (IBKR)")
            log_shadow_trade(symbol, "SELL", execution_price, "Signal from IBKR")
        else:
            print(f"[{symbol}] ⚪ Ignoring SELL — not held (IBKR)")
    else:
        print(f"[{symbol}] ⏸ HOLD — no signal (IBKR)")

print(f"{'='*10} End of Recs for {today} {'='*10}\n")
ib.disconnect()