# Migration Guide: CurrenSeaBot → MarketCalendarBot

## Overview Comparison

| Aspect | CurrenSeaBot (Node.js) | MarketCalendarBot (Python) |
|--------|----------------------|--------------------------|
| **Language** | JavaScript (Node.js) | Python 3.11+ |
| **Package Manager** | npm | uv |
| **Main Purpose** | Currency exchange rates | Market opening calendars |
| **Data Source** | External API (exchangerate.fun) | Local calendars (exchange_calendars) |
| **Notification** | Telegram | Telegram |
| **Deployment** | GitHub Actions | GitHub Actions |
| **Schedule** | Configurable cron | Configurable cron |

## Project Structure

### CurrenSeaBot Structure
```
CurrenSeaBot/
├── index.js                 # Main logic
├── package.json             # Dependencies
├── .env.example             # Configuration template
├── .github/
│   └── workflows/
│       └── action.yml       # GitHub Actions workflow
└── README.md
```

### MarketCalendarBot Structure
```
MarketCalendarBot/
├── main.py                  # Main bot logic
├── config.py                # Configuration management
├── test_main.py             # Unit tests
├── pyproject.toml           # Project metadata & dependencies
├── .env.example             # Configuration template
├── Makefile                 # Development commands
├── setup.sh                 # Setup script
├── .github/
│   └── workflows/
│       └── market-calendar.yml  # GitHub Actions workflow
└── README.md
```

## Configuration Comparison

### Environment Variables

**CurrenSeaBot:**
```env
TELEGRAM_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
CURRENSEA_BASE=USD
CURRENSEA_SYMBOL=SGD
```

**MarketCalendarBot:**
```env
TELEGRAM_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
MARKET_CALENDAR_EXCHANGES=NYSE,LSE,TSE,SGX
TIMEZONE=UTC
```

## Code Architecture

### CurrenSeaBot (Imperative Flow)
1. Load environment variables
2. Validate required env vars
3. Fetch exchange rate from API
4. Parse response
5. Send to Telegram
6. Exit

```javascript
const fetchCurrencyRate = async () => {
  // Fetch from external API
  const response = await fetch(url);
  const data = await response.json();
  return data.rates[quoteCurrency];
};

const sendTelegramMessage = async (message) => {
  // POST to Telegram API
};

const main = async () => {
  const rate = await fetchCurrencyRate();
  await sendTelegramMessage(msg);
};
```

### MarketCalendarBot (Modular Architecture)
1. Load configuration from env
2. Validate configuration
3. Query local market calendars
4. Format next market opens
5. Send to Telegram
6. Exit with status

```python
def fetch_next_session(exchange: str) -> dict | None:
    """Fetch the next market open for an exchange."""
    # Uses exchange_calendars library locally
    
async def send_telegram_message(message: str) -> bool:
    # Send to Telegram API
    
async def main():
    # Orchestrate the flow
```

## Deployment

### GitHub Actions

**CurrenSeaBot:**
- Uses `actions/setup-node`
- Runs `npm ci` for dependencies
- Schedule: `0 16 * * *` (4 PM UTC daily)

**MarketCalendarBot:**
- Uses `astral-sh/setup-uv` (official uv action)
- Runs `uv sync --frozen` for dependencies
- Schedule: `0 8 * * 1-5` (8 AM UTC on weekdays)
- Includes automatic Python 3.11 setup

## Key Differences

### 1. Data Handling
- **CurrenSeaBot**: Calls external API for real-time data
- **MarketCalendarBot**: Uses bundled market calendar data (exchange_calendars library)

### 2. Performance
- **CurrenSeaBot**: 1-2 seconds (depends on API latency)
- **MarketCalendarBot**: 1-2 seconds (local calendar lookups + Telegram)

### 3. Reliability
- **CurrenSeaBot**: May fail if external API is down
- **MarketCalendarBot**: More resilient (data bundled with library)

### 4. Configurability
- **CurrenSeaBot**: Fixed to 2 currencies (base/symbol)
- **MarketCalendarBot**: Multiple exchanges via comma-separated list

### 5. Error Handling
- **CurrenSeaBot**: Basic try-catch with `process.exit(1)`
- **MarketCalendarBot**: Structured error handling with validation

## Migration Workflow

If you want to migrate existing infrastructure:

1. **GitHub Actions**: Update workflow file to use `astral-sh/setup-uv`
2. **Secrets/Variables**: Update GitHub credentials
3. **Dependencies**: Ensure Python 3.11+ available in runners
4. **Testing**: Run `make test` locally before deployment
5. **Monitoring**: Update alert routing if different from CurrenSeaBot

## Advantages of MarketCalendarBot

✅ **No External Dependencies**: Market data bundled with library
✅ **Multiple Exchanges**: Configure many markets at once
✅ **Rich Ecosystem**: Python data science libraries for extensions
✅ **Testing Framework**: Includes pytest setup
✅ **Development Tools**: Makefile, setup script provided
✅ **Type Safety**: Configuration dataclass with validation
✅ **Better Async Support**: AsyncIO for future scalability

## Extending MarketCalendarBot

### Add Market Close Times
```python
def fetch_next_close(exchange: str) -> dict | None:
    # Similar to fetch_next_session but uses close times
```

### Add Market Holiday Detection
```python
def is_market_closed(exchange: str, date) -> bool:
    calendar = xcals.get_calendar(exchange)
    return date not in calendar.sessions
```

### Add Multiple Notification Channels
```python
async def send_discord_webhook(message: str):
    # Add Discord notifications
    
async def send_slack_message(message: str):
    # Add Slack notifications
```

### Add Web Webhook
```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/trigger")
async def trigger_bot():
    return await main()
```

## Troubleshooting Migration

| Issue | Solution |
|-------|----------|
| Python not found | Use `astral-sh/setup-uv` action in GitHub Actions |
| Import errors | Run `uv sync` to ensure all dependencies installed |
| Old node_modules | GitHub Actions automatically uses uv cache |
| Telegram messages failing | Verify secrets are set, not variables |

## Next Steps

1. **Local Testing**: `make run` to test locally
2. **GitHub Setup**: Add secrets/variables to your repo
3. **Custom Exchanges**: Edit `MARKET_CALENDAR_EXCHANGES` in `.env`
4. **Custom Schedule**: Edit cron in `.github/workflows/market-calendar.yml`
5. **Extensions**: See "Extending MarketCalendarBot" section above
