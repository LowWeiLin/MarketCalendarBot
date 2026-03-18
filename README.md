# Market Calendar Bot

A Telegram bot that sends scheduled alerts for market session times using the `pandas_market_calendars` library.

## Features

- 📅 Checks upcoming market opens/closes for configured exchanges
- 🤖 Sends alerts via Telegram
- ⏰ Runs on configurable cron schedule
- 🌍 Supports exchanges from `pandas_market_calendars`
- 🔧 Easy to configure with environment variables
- 🧪 Includes tests and development utilities

## Supported Exchanges

Visit the [pandas_market_calendars documentation](https://github.com/rsheftel/pandas_market_calendars) for a complete list of supported exchanges. Common ones include:

- `NYSE` - New York Stock Exchange
- `LSE` - London Stock Exchange
- `XSES` - Singapore Exchange
- `JPX` - Japan Exchange Group
- `ASX` - Australian Securities Exchange
- `BME` - Madrid Stock Exchange
- `HKEX` - Hong Kong Exchanges and Clearing
- `CME` - Chicago Mercantile Exchange
- `EUREX` - European Exchange
- And many more...

## Prerequisites

- Python 3.11+
- `uv` package manager ([install](https://docs.astral.sh/uv/getting-started/installation/))
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- Telegram Chat ID

## Setup

### 1. Get Telegram Credentials

1. Open Telegram and find [@BotFather](https://t.me/BotFather)
2. Send `/newbot` to create a new bot
3. Follow the prompts and note your bot token
4. To get your Chat ID, send a message to your bot and visit:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
   Look for the `chat.id` in the response

### 2. Clone and Setup

```bash
git clone <repo-url>
cd market-calendar-bot
```

### 3. Install Dependencies using uv

```bash
# Using setup script (Unix/Linux/Mac)
bash setup.sh

# Or manually
uv sync
```

### 4. Configure Environment

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
MARKET_CALENDAR_EXCHANGES=NYSE,LSE,XSES,HKEX
TIMEZONE=America/New_York
```

**Configuration Options:**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_TOKEN` | Yes | - | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Yes | - | Your Telegram chat ID |
| `MARKET_CALENDAR_EXCHANGES` | Yes | - | Comma-separated exchange codes |
| `TIMEZONE` | Yes | - | Timezone for display (e.g., `America/New_York`, `Europe/London`) |

## Usage

### Run Locally

```bash
# Install dependencies
uv sync

# Run the bot once
uv run main.py

# Or using make
make run
```

### Development Commands

```bash
# Install with dev dependencies
make dev

# Run tests
make test

# Run linting checks
make lint

# Clean cache files
make clean

# Show all available commands
make help
```

## GitHub Actions Setup

This project includes a GitHub Actions workflow for automated scheduled runs.

### Required Secrets

Set these in your GitHub repository settings under **Secrets and variables → Actions**:

- `TELEGRAM_TOKEN` - Your Telegram bot token
- `TELEGRAM_CHAT_ID` - Your Telegram chat ID

### Configuration Variables

Set these in **Settings → Variables → Actions**:

- `MARKET_CALENDAR_EXCHANGES` - Comma-separated list (e.g., `NYSE,LSE,XSES`)
- `TIMEZONE` - Display timezone (e.g., `America/New_York`)

### Default Schedule

The workflow runs at **8 AM UTC on weekdays**. To change the schedule, edit `.github/workflows/market-calendar.yml`:

```yaml
on:
  schedule:
    - cron: "0 8 * * 1-5"  # 8 AM UTC, Monday-Friday
```

Cron format: `minute hour day month day-of-week`

### Manual Trigger

The workflow can also be triggered manually from the GitHub Actions tab.

## Project Structure

```
market-calendar-bot/
├── main.py                          # Main bot logic
├── config.py                        # Configuration management
├── test_main.py                     # Unit tests
├── pyproject.toml                   # Project metadata and dependencies
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
├── Makefile                         # Development commands
├── setup.sh                         # Setup script
├── README.md                        # This file
└── .github/
    └── workflows/
        └── market-calendar.yml      # GitHub Actions workflow
```

## Development

### Adding New Features

1. Create a feature branch
2. Make your changes
3. Run tests: `make test`
4. Submit a pull request

### Testing

```bash
# Run all tests
make test

# Run specific test
uv run pytest test_main.py::test_fetch_next_session_valid_exchange -v
```

### Linting

```bash
# Check code style
make lint

# Or manually
uv run ruff check .
```

## Troubleshooting

### Bot doesn't send messages
- Verify `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` are correct
- Check that the bot has permission to send messages in the chat
- Look at the console output for error messages

### Exchange not found
- Verify the exchange code is valid (check [pandas_market_calendars docs](https://github.com/rsheftel/pandas_market_calendars))
- Some exchanges may not have data for certain date ranges

### Import errors
- Make sure you're using the correct Python environment: `uv run` handles this automatically

## Performance

- Each market calendar check: ~1-2 seconds
- Telegram message send: ~1-2 seconds
- Total runtime: typically < 5 seconds (well under GitHub Actions 5-minute timeout)

## License

ISC

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions:
1. Check [exchange_calendars repository](https://github.com/gerrymanoim/exchange_calendars)
2. Review GitHub Actions logs for errors
3. Check Telegram bot permissions and token validity

