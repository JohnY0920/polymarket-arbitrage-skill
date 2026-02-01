# Polymarket Arbitrage Skill

A Clawdbot/OpenClaw skill for monitoring and executing arbitrage opportunities on Polymarket prediction markets.

## 🎯 What This Does

Automatically detects three types of arbitrage on Polymarket:

1. **Math Arbitrage** - Multi-outcome markets where probabilities don't sum to 100%
2. **Cross-Market Arbitrage** - Same event priced differently across markets
3. **Orderbook Arbitrage** - Bid/ask spread inefficiencies

Includes built-in risk management, fee calculations, and paper trading mode.

## 🚀 Quick Start

### Installation

1. **Install the skill** (if using Clawdbot):
   ```bash
   clawdbot skills install polymarket-arbitrage.skill
   ```

2. **Or use standalone**:
   ```bash
   git clone https://github.com/JohnY0920/polymarket-arbitrage-skill.git
   cd polymarket-arbitrage-skill/skills/polymarket-arbitrage
   pip install requests beautifulsoup4
   ```

### Run First Scan

```bash
python3 scripts/monitor.py --once --min-edge 3.0
```

This will scan Polymarket and save any arbitrage opportunities to `polymarket_data/arbs.json`.

### Continuous Monitoring

```bash
python3 scripts/monitor.py --interval 300 --min-edge 3.0
```

Scans every 5 minutes and alerts on new opportunities.

## 📊 What to Expect

**Reality check:** Polymarket is an efficient market. Real arbitrage opportunities are rare.

- **Good arbs:** 1-3 per week (if you're lucky)
- **Typical edge:** 0.5-2% net profit after fees
- **Execution rate:** 60-70% (many disappear before you can trade)
- **Competition:** Professional bots capture arbs in milliseconds

**This is NOT get-rich-quick.** It's grinding small edges and learning quantitative trading.

## 🛠️ Components

### Scripts

- **fetch_markets.py** - Scrape Polymarket for market data
- **detect_arbitrage.py** - Find arbitrage opportunities (accounts for 2% fees)
- **monitor.py** - Continuous monitoring with deduplication and alerts

### References

- **arbitrage_types.md** - Deep dive on the 3 types of arbitrage with examples
- **getting_started.md** - Step-by-step guide from paper trading to real money

### Features

- ✅ Automatic fee calculation (2% Polymarket taker fee)
- ✅ Risk scoring (0-100, lower is better)
- ✅ Volume filtering (focus on liquid markets)
- ✅ Deduplication (avoid duplicate alerts)
- ✅ Paper trading mode (no real money)
- ✅ Timestamped data snapshots

## 📈 Recommended Workflow

### Phase 1: Paper Trading (Week 1-2)

Run monitor 2-3x per day and track opportunities in a spreadsheet.

**Goal:** Understand opportunity frequency and quality.

### Phase 2: Micro Testing ($50-100)

If seeing 3-5 opportunities per week:
- Create Polymarket account
- Deposit small amount
- Manual trades only, max $5-10 each

**Goal:** Learn platform mechanics.

### Phase 3: Scale Up ($500+)

If profitable after 20+ trades:
- Increase bankroll
- Max 5% per trade
- Implement strict risk management

**Goal:** Consistent profitability.

### Phase 4: Automation (Future)

Only if consistently profitable (>10% monthly ROI). Requires:
- Polymarket API integration or browser automation
- Wallet integration (private key management)
- Order execution logic

## ⚠️ Risk Management

**Critical rules:**

1. **Max position size:** 5% of bankroll per opportunity
2. **Minimum edge:** 3% net profit (after fees)
3. **Daily loss limit:** 10% of bankroll
4. **Focus on buy arbs:** Safer than sell-side (which requires capital/liquidity)

## 💰 Fee Structure

Polymarket charges:
- **Maker fee:** 0%
- **Taker fee:** 2%

**Breakeven threshold:**
- 2-outcome market: Need >4% gross edge (2% × 2 legs)
- 3-outcome market: Need >6% gross edge
- N-outcome market: Need >2N% gross edge

**Recommended minimum:** 3-5% net profit after fees.

## 📖 Documentation

Full documentation in:
- `skills/polymarket-arbitrage/SKILL.md` - Complete skill guide
- `references/arbitrage_types.md` - Strategy explanations
- `references/getting_started.md` - Setup and workflow
- `polymarket-arbitrage-README.md` - Detailed README

## 🔧 Advanced Usage

### Custom Edge Threshold

```bash
python3 scripts/monitor.py --min-edge 5.0  # Higher quality, fewer opportunities
```

### Volume Filtering

```bash
python3 scripts/fetch_markets.py --min-volume 1000000  # $1M+ only
```

### Webhook Alerts (Future)

```bash
python3 scripts/monitor.py --alert-webhook "https://api.telegram.org/bot<token>/sendMessage?chat_id=<id>"
```

## 🐛 Troubleshooting

### "No arbitrages found"

**Normal!** Polymarket is efficient. Try:
- Lower `--min-edge` to 2.0
- Run during major news events
- Check smaller markets (riskier)

### "High edge but disappeared"

**Expected.** Homepage prices lag the orderbook. Bots capture arbs in milliseconds.

### "Can't execute at displayed price"

**Liquidity issue.** Stick to $1M+ volume markets.

## 📚 Resources

- **Polymarket:** https://polymarket.com
- **Polymarket Docs:** https://docs.polymarket.com
- **ClawdHub (skill directory):** https://clawdhub.com
- **Clawdbot Docs:** https://docs.clawd.bot

## ⚖️ License

MIT License - See LICENSE file

## ⚠️ Disclaimer

**This software is for educational purposes only.**

- Not financial advice
- Real risk of loss
- You're competing with professional traders
- Only invest what you can afford to lose
- Built by an AI (JoJo) for learning quantitative trading strategies

**Trading involves risk. Past performance does not guarantee future results.**

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch
3. Test thoroughly
4. Submit a pull request

## 📧 Contact

- **GitHub:** [@JohnY0920](https://github.com/JohnY0920)
- **Issues:** https://github.com/JohnY0920/polymarket-arbitrage-skill/issues

---

Built with ❤️ by JoJo (AI assistant) for John Yin  
Version: 1.0  
Date: February 2026
