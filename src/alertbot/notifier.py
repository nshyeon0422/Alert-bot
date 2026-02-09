from __future__ import annotations

import logging
import time

import requests

from .config import Config
from .parser import ParsedItem

LOGGER = logging.getLogger(__name__)


def send_telegram(item: ParsedItem, config: Config) -> None:
    if not config.telegram_bot_token or not config.telegram_chat_id:
        raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required")

    message = item.title
    if item.link:
        message = f"{item.title}\n{item.link}"

    url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": config.telegram_chat_id,
        "text": message,
        "disable_web_page_preview": True,
    }

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    LOGGER.info("Sent Telegram alert for: %s", item.title)
    time.sleep(max(config.telegram_send_delay_seconds, 0))


def send_startup_message(config: Config) -> None:
    if not config.telegram_bot_token or not config.telegram_chat_id:
        raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required")

    url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": config.telegram_chat_id,
        "text": "✅ 모니터링 시작됨",
        "disable_web_page_preview": True,
    }

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    LOGGER.info("Sent startup message")
    time.sleep(max(config.telegram_send_delay_seconds, 0))
