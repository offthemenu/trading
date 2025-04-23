# Market Data Subscriptions for Live IBKR Trading

This document outlines the **minimal real-time market data feeds** required to fully enable autonomous trading with the current ETF watchlist. These feeds are needed to:

- Access live bid/ask/mid pricing for limit order execution
- Evaluate real-time market signals
- Prevent trading on stale or delayed data

---

## ✅ Current Watchlist

| Ticker | Description | Primary Exchange | Required Feed |
|--------|-------------|------------------|----------------------------|
| QQQM   | Invesco NASDAQ 100 ETF        | NASDAQ    | NASDAQ Level I (Top-of-Book) |
| VOO    | Vanguard S&P 500 ETF          | NYSE Arca | NYSE Arca Level I            |
| IAU    | iShares Gold Trust            | NYSE Arca | NYSE Arca Level I            |
| IEFA   | iShares Intl Developed Markets| Cboe BATS | Cboe One Summary             |
| MCHI   | iShares China ETF             | NASDAQ    | NASDAQ Level I               |
| BOTZ   | Global Robotics & AI ETF      | NYSE Arca | NYSE Arca Level I            |
| ROBO   | ROBO Global Robotics & Auto   | NASDAQ    | NASDAQ Level I               |

---

## 🧾 Subscription Plan (API-Compatible Only)

You only need the following **API-enabled subscriptions**:

1. **NASDAQ Level I (Top-of-Book)**  
   For: `QQQM`, `MCHI`, `ROBO`  
   📈 Exchange: NASDAQ  
   💵 Estimated Cost: ~$1.50–$3/month

2. **NYSE Arca Level I (Top-of-Book)**  
   For: `VOO`, `IAU`, `BOTZ`  
   📈 Exchange: NYSE Arca  
   💵 Estimated Cost: ~$1.50–$3/month

3. **Cboe One Summary** or **BATS Top-of-Book**  
   For: `IEFA`  
   📈 Exchange: Cboe BATS  
   💵 Estimated Cost: ~$2–$5/month

---

## 💰 Estimated Total Monthly Cost

**~$5 to $11/month**  
(based on individual exchange subscriptions — far cheaper than the $125 “US Equity Bundle”)

---

## 📌 Notes

- Be sure to select **“API-Enabled”** versions of each feed.
- These are available under:  
  👉 `IBKR Client Portal → Settings → Market Data Subscriptions`
- Once active, your trading agent can:
  - Pull live bid/ask spreads
  - Place precise limit orders
  - Monitor fill health and trade quality

---

_Last updated: April 2025_