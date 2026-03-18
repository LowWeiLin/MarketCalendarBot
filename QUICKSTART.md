# Quick Start Guide

Get the Market Calendar Bot running in 5 minutes.

## 1. Prerequisites

```bash
# Check if uv is installed
uv --version

# If not installed:
# https://docs.astral.sh/uv/getting-started/installation/
```

## 2. Clone & Setup

```bash
cd C:\Users\lwl19\Documents\Code\2026\MarketCalendarBot

# Windows (PowerShell or Command Prompt)
copy .env.example .env

# Or Unix/Linux/Mac
cp .env.example .env
```

## 3. Configure

Edit `.env` with your credentials:

```env
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
MARKET_CALENDAR_EXCHANGES=NYSE,LSE,XSES
TIMEZONE=America/New_York
```

**How to get Telegram credentials:**

1. Open Telegram → [@BotFather](https://t.me/BotFather)
2. `/newbot` to create a new bot
3. Copy the token to `TELEGRAM_TOKEN`
4. Send a message to your bot, then visit:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
5. Find `chat.id` and copy to `TELEGRAM_CHAT_ID`

## 4. Test Locally

```bash
# Install dependencies
uv sync

# Run once
uv run main.py

# You should see market open times printed and a Telegram message sent!
```

## 5. Deploy to GitHub Actions

1. Push to GitHub
2. Go to repo **Settings → Secrets and variables → Actions**
3. Add secrets:
   - `TELEGRAM_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. Add variables (optional):
   - `MARKET_CALENDAR_EXCHANGES`
   - `TIMEZONE`
5. Done! Workflow will run at 8 AM UTC on weekdays

## Common Commands

```bash
make run      # Run the bot once
make test     # Run tests
make install  # Install dependencies
make dev      # Install with dev tools
make clean    # Clean cache
make help     # Show all commands
```

## Supported Exchanges

Use exchange names from [pandas_market_calendars](https://github.com/rsheftel/pandas_market_calendars), for example:

- `NYSE` - New York Stock Exchange
- `LSE` - London Stock Exchange
- `XSES` - Singapore Exchange
- `HKEX` - Hong Kong Exchanges and Clearing
- `JPX` - Japan Exchange Group

You can list all supported exchange names locally with:

```bash
uv run python -c "import pandas_market_calendars as mcal; print(mcal.get_calendar_names())"
```

## Customize Schedule

Edit `.github/workflows/market-calendar.yml`:

```yaml
on:
  schedule:
    - cron: "0 8 * * 1-5"  # Change this line
```

Cron format: `minute hour day-of-month month day-of-week`

Examples:
- `0 8 * * 1-5` - Every weekday at 8 AM
- `0 9 * * 0` - Every Sunday at 9 AM
- `30 16 * * *` - Every day at 4:30 PM

## Next Steps

1. ✅ Test locally with `make run`
2. ✅ Push to GitHub
3. ✅ Add secrets to GitHub
4. ✅ Wait for first scheduled run
5. ✅ Check Telegram for messages!

## Troubleshooting

**Bot doesn't send messages:**
- Check `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`
- Verify you can message the bot directly
- Run `uv run main.py` and check console output

**"No markets opening today":**
- This is normal on weekends/holidays
- The bot correctly skips non-trading days

**Import errors:**
- Run `uv sync` to ensure dependencies are installed
- Check `.env` is not corrupted

**GitHub Actions fails:**
- Check workflow logs: **Actions → Failed Run → Logs**
- Verify secrets are set (not variables!)
- Ensure Python 3.11+ available in runner

## Need Help?

1. Check the [full README](README.md)
2. Read [MIGRATION.md](MIGRATION.md) for architecture details
3. Visit [pandas_market_calendars](https://github.com/rsheftel/pandas_market_calendars) for calendar issues
4. Check GitHub Actions logs for detailed errors
