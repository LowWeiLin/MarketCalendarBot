import os
import asyncio
import re
from datetime import datetime, timedelta
import pytz
import pandas as pd
import pandas_market_calendars as mcal
from dotenv import load_dotenv

load_dotenv()

TIMEZONE = os.getenv("TIMEZONE", "").strip()
MARKET_CALENDAR_EXCHANGES = os.getenv("MARKET_CALENDAR_EXCHANGES", "").split(",")

TIMEZONE_ALIASES = {
    "UTC": "UTC",
    "GMT": "UTC",
    "PST": "America/Los_Angeles",
    "PDT": "America/Los_Angeles",
    "EST": "America/New_York",
    "EDT": "America/New_York",
    "CST": "America/Chicago",
    "CDT": "America/Chicago",
    "MST": "America/Denver",
    "MDT": "America/Denver",
}


def _parse_fixed_offset_timezone(timezone_name: str):
    match = re.fullmatch(
        r"(?:UTC|GMT)\s*([+-])\s*(\d{1,2})(?::?(\d{2}))?",
        timezone_name.strip(),
        re.IGNORECASE,
    )

    if not match:
        return None

    sign, hours_text, minutes_text = match.groups()
    hours = int(hours_text)
    minutes = int(minutes_text or "0")

    if hours > 14 or minutes > 59:
        return None

    offset_minutes = (hours * 60) + minutes
    if sign == "-":
        offset_minutes *= -1

    label = f"UTC{sign}{hours:02d}:{minutes:02d}"
    return pytz.FixedOffset(offset_minutes), label


def _resolve_timezone(timezone_name: str):
    normalized_name = TIMEZONE_ALIASES.get(timezone_name.upper(), timezone_name)

    fixed_offset = _parse_fixed_offset_timezone(normalized_name)
    if fixed_offset:
        return fixed_offset

    try:
        return pytz.timezone(normalized_name), normalized_name
    except Exception:
        print(f"Invalid TIMEZONE '{timezone_name}', falling back to UTC")
        return pytz.timezone("UTC"), "UTC"


DISPLAY_TZ, DISPLAY_TIMEZONE_NAME = _resolve_timezone(TIMEZONE)


def _to_display_datetime(value: pd.Timestamp | None, tz) -> datetime | None:
    if value is None or pd.isna(value):
        return None
    if value.tzinfo is None:
        value = value.tz_localize("UTC")
    return value.tz_convert(tz).to_pydatetime()


def _format_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M")


def _format_open_hours(next_open: datetime, next_close: datetime) -> str:
    total_hours = (next_close - next_open).total_seconds() / 3600

    rounded_hours = round(total_hours, 1)
    if rounded_hours.is_integer():
        return f"{int(rounded_hours)}h"
    return f"{rounded_hours}h"


def fetch_next_session(exchange: str) -> dict | None:
    """Fetch the next market session times for a given exchange."""
    try:
        calendar = mcal.get_calendar(exchange)
        now = datetime.now(DISPLAY_TZ)
        today = now.date()

        # Get the next session (looking 30 days ahead)
        end_date = today + timedelta(days=30)
        schedule = calendar.schedule(start_date=today, end_date=end_date)

        for _, session in schedule.iterrows():
            next_open = _to_display_datetime(session.get("market_open"), DISPLAY_TZ)
            next_close = _to_display_datetime(session.get("market_close"), DISPLAY_TZ)

            if not next_open or not next_close:
                continue

            if next_open > now:
                return {
                    "exchange": exchange,
                    "next_open": next_open,
                    "next_close": next_close,
                    "timezone": DISPLAY_TIMEZONE_NAME,
                }

        return None
    except Exception as e:
        print(f"Error fetching calendar for {exchange}: {e}")
        return None


async def send_telegram_message(message: str) -> bool:
    """Send a message via Telegram."""
    import urllib.request
    import json

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not telegram_token or not telegram_chat_id:
        raise RuntimeError(
            "TELEGRAM_TOKEN and TELEGRAM_CHAT_ID environment variables required"
        )

    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

    try:
        data = json.dumps(
            {
                "chat_id": telegram_chat_id,
                "text": message,
            }
        ).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            response_data = json.loads(response.read().decode("utf-8"))
            if not response_data.get("ok"):
                print(f"Telegram error: {response_data.get('description')}")
                return False
            return True
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
        return False


async def main():
    """Main function to fetch market calendar info and send alerts."""
    # Validate required env vars at runtime
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    missing = []
    if not telegram_token:
        missing.append("TELEGRAM_TOKEN")
    if not telegram_chat_id:
        missing.append("TELEGRAM_CHAT_ID")
    if not TIMEZONE:
        missing.append("TIMEZONE")
    if not any(ex.strip() for ex in MARKET_CALENDAR_EXCHANGES):
        missing.append("MARKET_CALENDAR_EXCHANGES")
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    exchanges = [ex.strip() for ex in MARKET_CALENDAR_EXCHANGES if ex.strip()]

    print(f"Fetching next market session times for: {', '.join(exchanges)}")

    results = []
    for exchange in exchanges:
        result = fetch_next_session(exchange)
        if result:
            results.append(result)

    if not results:
        print("No upcoming market sessions found")
        return

    # Build message
    message_lines = [
        f"📅 Market Calendar - Next Session Times ({DISPLAY_TIMEZONE_NAME}):",
        "",
    ]
    exchange_width = max(len(result["exchange"]) for result in results)

    for result in results:
        open_time = _format_datetime(result["next_open"])
        close_time = _format_datetime(result["next_close"])
        hours_open = _format_open_hours(result["next_open"], result["next_close"])

        line = f"{result['exchange']:>{exchange_width}}: Open {open_time} ➡️ Close {close_time}"

        line += f" ({hours_open})"
        message_lines.append(line)

    message = "\n".join(message_lines)
    print(f"Sending message:\n{message}")

    success = await send_telegram_message(message)
    if success:
        print("Message sent successfully!")
    else:
        print("Failed to send message")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
