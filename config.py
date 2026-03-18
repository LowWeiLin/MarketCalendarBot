"""
Configuration schemas and utilities for market calendar bot.

This module provides typed configurations to ensure valid setups.
"""

from dataclasses import dataclass
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotConfig:
    """Configuration for the market calendar bot."""

    telegram_token: str
    telegram_chat_id: str
    exchanges: List[str]
    timezone: str

    @classmethod
    def from_env(cls) -> "BotConfig":
        """Load configuration from environment variables."""
        token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        exchanges_str = os.getenv("MARKET_CALENDAR_EXCHANGES", "NYSE,LSE")
        timezone = os.getenv("TIMEZONE", "UTC")

        if not token:
            raise ValueError("TELEGRAM_TOKEN environment variable not set")
        if not chat_id:
            raise ValueError("TELEGRAM_CHAT_ID environment variable not set")

        exchanges = [ex.strip() for ex in exchanges_str.split(",") if ex.strip()]

        return cls(
            telegram_token=token,
            telegram_chat_id=chat_id,
            exchanges=exchanges,
            timezone=timezone,
        )

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.telegram_token:
            raise ValueError("Telegram token cannot be empty")
        if not self.telegram_chat_id:
            raise ValueError("Telegram chat ID cannot be empty")
        if not self.exchanges:
            raise ValueError("At least one exchange must be configured")
        return True
