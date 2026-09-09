# Ai-Automated-Trading-Agents

### Agents
1. Market scout... Searches for whats happening across the market

2. Regime agent: determine whether the market is 
     STRONG_UPTREND
     WEAK_UPTREND
     SIDEWAYS
     HIGH_VOLATILITY
     LOW_VOLATILITY
     DOWNTREND
     PANIC

3.Strategy Agent : different strategies should compete
     Momentum
     Mean Reversion
     Breakout
     Trend Following
     Statistical Arbitrage
     Market Making       


4. Risk Agent: this agent should have veto power
      Signal Agent:
     BUY BTC
     confidence = 82%

      Risk Agent:
     volatility = extreme
     portfolio exposure = high
     correlation = high

     DECISION:
        REJECT


5. Execution Agent: Determines
      market order?
      limit order?

      how much?
      where?
      slippage?
      fees?        


6. Performance Agent: After each trade, records
     What happened?

     Why did we enter?

     What was expected?

     What actually happened?

     Was the strategy correct?

     Was the execution bad?

     Was the market regime misclassified?      


## Phase 1
    build:
      MarketData
      Candle
      Order
      Position
      Portfolio
      Trade     


## phase 2
  Backtest:
    BTCUSDT
    2025-01-01
    2025-01-02
     ...      

And simulate :
    $1,000 starting capital

→ strategy
→ signals
→ orders
→ fees
→ slippage
→ positions
→ P&L

## Phase 3
  Risk Engine:
     before allowing a trade
       Signal
         ↓
      Risk Engine
         ↓
  Approved / Rejected


## Phase 4
     Paper-Trading but using virtual money


## Phase 5 
    — AI/ML layer:

Only after we have good data.

Then we can experiment with:

feature engineering
classification
probability estimation
regime detection
reinforcement-learning research
ensemble models
LLM-based reasoning/orchestration

The AI should augment the trading system, not magically replace statistical validation.

## Phase 6 — 
     Live crypto execution:

Only after:

Backtest
       ↓
Walk-forward test
       ↓
Paper trading
       ↓
Stress testing
       ↓
Risk validation
       ↓
Small live allocation     


Api key should allow trading permission only




             CRYPTO AI TRADING SYSTEM

                       │
             ┌─────────┴─────────┐
             │                   │
        MARKET SCANNER       NEWS/SENTIMENT
             │                   │
             └─────────┬─────────┘
                       │
                 REGIME AGENT
                       │
          ┌────────────┼────────────┐
          │            │            │
       MOMENTUM     BREAKOUT    MEAN-REV
          │            │            │
          └────────────┼────────────┘
                       │
                  META AGENT
                       │
                  RISK AGENT
                       │
                 EXECUTION
                       │
                    TRADE
                       │
                 PERFORMANCE
                       │
                  LEARNING
                       │
                       └──────► back to system


ai_trading_system/
│
├── app/
│   ├── main.py
│   │
│   ├── agents/
│   │   ├── market_agent.py
│   │   ├── trend_agent.py
│   │   ├── momentum_agent.py
│   │   ├── regime_agent.py
│   │   ├── decision_agent.py
│   │   ├── risk_agent.py
│   │   └── learning_agent.py
│   │
│   ├── strategies/
│   │   ├── momentum.py
│   │   ├── mean_reversion.py
│   │   ├── breakout.py
│   │   └── arbitrage.py
│   │
│   ├── data/
│   │   ├── market_data.py
│   │   ├── websocket.py
│   │   └── database.py
│   │
│   ├── execution/
│   │   ├── broker.py
│   │   ├── paper_trader.py
│   │   └── live_trader.py
│   │
│   ├── risk/
│   │   ├── position_sizing.py
│   │   ├── portfolio_risk.py
│   │   └── risk_limits.py
│   │
│   ├── backtesting/
│   │   ├── engine.py
│   │   ├── metrics.py
│   │   └── simulator.py
│   │
│   └── models/
│       ├── features.py
│       ├── predictor.py
│       └── training.py
│
├── tests/
│
├── notebooks/
│
├── data/
│
├── .env
├── requirements.txt
└── README.md


Milestone 2 — Time-Series Gap Detection

Integration completed

Added CandleGapDetector
Detects missing intervals without modifying the original data
Supports arbitrary candle intervals through timedelta

Key project decisions

Missing data is different from invalid data.
Gaps are detected, not silently repaired.
No synthetic candles are created at the data-ingestion layer.
The interval is supplied explicitly rather than hardcoded to 1 minute.
Gap information will later be available to the backtester and AI feature pipeline.
Updated architecture
Raw Market Data
      │
      ▼
    Candle
      │
      ▼
CandleValidator
      │
      ▼
Timestamp Integrity
      │
      ▼
CandleGapDetector
      │
      ├── valid continuous data
      │
      └── gap information
                │
                ▼
        Data Quality Metadata
                │
        ┌───────┼────────┐
        ▼       ▼        ▼
    Indicators  AI    Backtester



    Milestone 3 — MarketData + Gap Detection Integration

Integrated

Candle
  ↓
CandleValidator
  ↓
MarketData
  ↓
CandleGapDetector
  ↓
Data-quality information

Key project decision:
The market-data layer will detect data problems but will not automatically repair them.

That is important for a trading system. We don't want the system inventing a candle because one is missing. Later, another component can decide whether a gap means:

ignore the period,
request the missing data,
invalidate a backtest segment,
reduce confidence,
or block trading temporarily.
Next milestone

We should now move from in-memory market data → persistent market data.

I recommend SQLite first because:

Python-only (sqlite3 is built in)
no separate database server
reliable transactions
excellent for our development/backtesting stage
easy to migrate to PostgreSQL later if the system grows

The next architecture will become:

Exchange / Historical Data
          ↓
    Exchange Adapter
          ↓
   Candle Validation
          ↓
      SQLite DB
          ↓
     MarketData
          ↓
   Gap / Quality Checks
          ↓
     Backtesting
          ↓
       Strategies
          ↓
     Risk Manager
          ↓
      Execution


      ### SQLite Database

I use SqLite database because its built into python and gives an advantage 



SQLite's REAL type is appropriate for our initial implementation.

Later, when we get into financial precision, we'll need to revisit how we represent prices and quantities. We should not blindly rely on binary floating-point for actual order accounting.

That's something we'll address before live trading.

Milestone 4A — Persistent Read/Write

Integrated:
Candle ↔ SQLite conversion, candle persistence, chronological retrieval, symbol/timeframe filtering.

Key decision:
The database layer returns domain objects (Candle) rather than raw database rows.

That keeps SQL concerns inside the database layer and lets the rest of our trading system work with clean Python objects.


Milestone 4B — Documentation

Integration

SQLite
 ├── Symbol isolation
 ├── Timeframe isolation
 ├── Timestamp uniqueness
 └── Chronological retrieval

Key project decision:
The database itself must enforce fundamental data-integrity rules wherever possible. We don't rely entirely on Python application logic.

Why:
Our trading engine may eventually have several data-ingestion processes. If two processes accidentally attempt to store the same candle, the database constraint protects us.

Current foundation:

                 Candle
                    │
                    ▼
             CandleValidator
                    │
                    ▼
               MarketData
                    │
                    ▼
             MarketDatabase
                    │
                    ▼
                 SQLite


                 Milestone 4C — Persistent MarketData Integration

Integrated:

MarketData ↔ MarketDatabase ↔ SQLite

Key decision: MarketData works with Candle objects; database-specific SQL remains inside MarketDatabase.

What this enables:

Historical data
      ↓
SQLite
      ↓
MarketData
      ↓
Backtesting

### Key project decision:

The database is the source of persistent truth, while MarketData provides the in-memory working layer. We never silently allow RAM and persistent storage to diverge.

###  Key architectural decision

Historical data retrieval must happen at the database/query layer rather than loading the entire dataset into memory and filtering it in Python.

That's important because our eventual AI trading system may process millions of candles.