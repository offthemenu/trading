from strategies.defensive_strategy import generate_signals
from utils.portfolio_io import read_positions, write_positions, log_trade, get_cash_available
import math

# Tickers we want to simulate over
WATCHLIST = ['QQQM', 'VOO', 'IAU', 'IEFA', 'MCHI']

def run_simulated_bot():
    print("🤖 Running simulated bot...")
    
    # Load existing portfolio from CSV
    positions = read_positions()
    
    # Keep a dict of latest prices for each ETF
    prices = {}
    trades_made = 0
    
    for ticker in WATCHLIST:
        # Get buy/sell signal + indicators for the current ETF
        signal = generate_signals(ticker)
        price = signal['price']
        prices[ticker] = price

        # Get current holding info (default to 0 if not in positions yet)
        current_position = positions.get(ticker, {'shares': 0, 'avg_price': 0})
        holding = current_position['shares'] > 0

        # ===================== BUY LOGIC ===================== #
        if signal['buy'] and not holding:
            # Determine how much we can invest: 20% of available capital
            cash_available = get_cash_available(positions, prices)
            max_trade_amount = cash_available * 0.2
            shares_to_buy = math.floor(max_trade_amount / price)  # Round down to whole shares

            if shares_to_buy > 0:
                # Update our positions record
                positions[ticker] = {
                    'shares': shares_to_buy,
                    'avg_price': price
                }
                # Log the simulated trade
                log_trade(ticker, 'BUY', price, shares_to_buy, 'Buy Signal Triggered')
                print(f"✅ BUY {shares_to_buy} shares of {ticker} @ ${price:.2f}")
                trades_made += 1

        # ===================== SELL LOGIC ===================== #
        elif signal['sell'] and holding:
            shares_to_sell = current_position['shares']
            
            # Log the sell event
            log_trade(ticker, 'SELL', price, shares_to_sell, 'Sell Signal Triggered')

            # Clear the position
            positions[ticker] = {'shares': 0, 'avg_price': 0}
            print(f"❌ SELL {shares_to_sell} shares of {ticker} @ ${price:.2f}")
            trades_made += 1
        
        # ===================== NO ACTION ===================== #
        else:
            print(f"No tradeaction for {ticker}.\n  Buy Signal: {signal['buy']}, Sell Signal: {signal['sell']}, Holding: {holding}\n")

    # Save updated positions back to file
    write_positions(positions)
    
    write_positions(positions)

    print("\n🔚 Simulation complete.")
    if trades_made == 0:
        print("📭 No trades were executed today.")
    else:
        print(f"📈 {trades_made} trade(s) logged.")

# 🏁 Main entrypoint
if __name__ == "__main__":
    run_simulated_bot()
