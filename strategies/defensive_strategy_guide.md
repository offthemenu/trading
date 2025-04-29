*Ver 1.0.0*

# 📖 Defensive Strategy - Study Guide

## Introduction

This trading strategy is designed to **minimize unnecessary trades** while **catching sustained upward trends** and **avoiding highly volatile conditions**.  
It is particularly tuned for **low-volatility index ETFs** (e.g., QQQM, VOO, IEFA) rather than volatile individual stocks.

The system uses a combination of **momentum**, **volatility filtering**, **volume confirmation**, and **mean-reversion protection** through the following indicators:

- Exponential Moving Averages (EMA 10 and EMA 50)
- Average True Range (ATR)
- Relative Strength Index (RSI)
- Volume SMA (20-day simple moving average)

---

## 🎯 Core Indicators

### 1. EMA10 vs EMA50 (Momentum)

- **EMA10** = short-term moving average (~2 weeks)
- **EMA50** = mid-term moving average (~2.5 months)
  
**Logic:**
- **Buy Signal:** If EMA10 > EMA50 → **short-term price momentum is bullish**.
- **Sell Signal:** If EMA10 < EMA50 → **momentum has reversed to bearish**.

This prevents you from buying into a downtrend.

---

### 2. ATR Ratio (Volatility Control)

- **ATR (14)** = measures daily price range variability over 14 days.
- **ATR Ratio** = ATR / Current Close Price

**Logic:**
- **Buy Allowed:** Only if ATR Ratio < 0.03 (**less than 3% daily movement**).
- **Sell Signal:** ATR Ratio > 0.03 triggers **exit**.

This ensures you're **only buying stable, non-erratic assets** — crucial for ETF-based strategies.

---

### 3. RSI (Overbought / Oversold Guardrails)

- **RSI (14)** = measures the speed and magnitude of price changes.

**Logic:**
- **Buy Allowed:** Only if 40 < RSI < 70.
- **Sell Signal:** RSI < 30 (oversold panic).

**Interpretation:**
- **RSI 40–70** → Moderate bullish momentum without being overbought.
- **Below 30 RSI** → Indicates breakdown, triggering immediate sell.
- **Above 70 RSI** is intentionally avoided for buys → prevents "buying tops".

---

### 4. Volume SMA (Confirmation Filter)

- **Volume SMA (20)** = 20-day average trading volume.

**Logic:**
- **Buy Allowed:** Only if today's volume > 20-day average.

**Why?**
- A breakout without above-average volume is often **a fakeout**.
- You want to see **increased participation** confirming the move.

---

## 🧠 Strategy Logic Flow

1. **Momentum Check:** Is EMA10 > EMA50? (Are we trending up?)
2. **Volatility Check:** Is ATR Ratio < 0.03? (Is the market calm?)
3. **Strength Check:** Is RSI between 40 and 70? (Are we moderately strong, not euphoric?)
4. **Volume Check:** Is today's volume > 20-day volume SMA? (Are others buying too?)

✅ If **all** are true → **Buy Signal**  
✅ If **any** major protection breaks (EMA reversal, ATR spike, RSI crash) → **Sell Signal**

---

## 🧹 Safety Features Baked In

| Feature | Why |
|:--------|:----|
| No Buy if High Volatility (ATR) | Avoid fake breakouts during chaos |
| No Buy if Overbought (RSI > 70) | Avoid buying tops |
| No Buy if Weak Volume | Avoid ghost breakouts |
| Forced Sell if RSI < 30 | Escape collapsing markets early |
| Forced Sell if ATR > 0.03 | Escape volatile collapses |
| Position Size Cap (20%) | Protect against portfolio wipeouts |

---

## 📈 Application to Your Watchlist

| Ticker | Description | Behavior Fit for Strategy |
|:-------|:------------|:---------------------------|
| QQQM | NASDAQ-100 Mini ETF | Slightly more volatile than VOO; ATR control important |
| VOO | S&P 500 ETF | Very stable; ideal for this system |
| IAU | Gold Trust ETF | Lower liquidity sometimes; volume filter helps |
| IEFA | Developed Intl ETF | Moderate; reacts to global events |
| MCHI | China ETF | Can spike in volatility; ATR essential |
| BOTZ | Robotics ETF | More growth exposure; EMA and ATR both critical |
| ROBO | Automation ETF | Similar to BOTZ; slightly steadier |
| FCG | Natural Gas ETF | Higher natural volatility; volume + ATR controls crucial |
| XOP | Oil & Gas ETF | Very volatile; this system will avoid most noisy breakouts |
| VGK | European ETF | Stable but can react to geopolitical news |
| EWJ | Japan ETF | Generally steady; good fit |

---

## 🔥 Strategic Goal

- **Capture stable uptrends**
- **Avoid chaotic whipsaws**
- **Exit early if market conditions worsen**
- **Limit maximum risk per asset**

Result: A system that is **slow, patient, and defensive**, built for **long-term compounded growth** without getting chopped up in short-term volatility.

---

## ⚡ In One Sentence

> **"Only buy when calm, trending, healthy volume is confirmed, and sell fast if storm clouds gather."**

---

# ✨ Closing Thought

This strategy isn't trying to "outsmart" the market.  
It's trying to **surf the easy waves** and **sit out the storms.**  
Exactly what a **defensive ETF investor** should aim for in a semi-automated system like yours.