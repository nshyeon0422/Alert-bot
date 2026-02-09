from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from alertbot.config import Config
from alertbot.fetcher import fetch_html
from alertbot.notifier import send_startup_message, send_telegram
from alertbot.parser import ParsedItem, parse_items
from alertbot.storage import Storage


def _matches_keywords(item: ParsedItem, keywords: list[str]) -> bool:
    if not keywords:
        return True
    haystack = f"{item.title} {item.content}".lower()
    return any(keyword.lower() in haystack for keyword in keywords)


def main() -> None:
    load_dotenv()
    config = Config.from_env()

    logging.basicConfig(level=config.log_level)

    if not config.target_url:
        raise ValueError("TARGET_URL is required")

    storage = Storage(config.state_db_path)
    send_startup_message(config)

    seed_only = config.seed_existing and storage.is_empty()

    while True:
        try:
            html = fetch_html(config)
            items = parse_items(html, config)
            for item in items:
                if config.use_keywords and not _matches_keywords(item, config.keywords):
                    continue
                if storage.is_seen(item):
                    continue
                if seed_only:
                    storage.mark_seen(item)
                    continue
                send_telegram(item, config)
                storage.mark_seen(item)
            seed_only = False
            storage.prune_keep_latest(config.max_items)
        except Exception as exc:  # noqa: BLE001
            logging.exception("Polling error: %s", exc)

        time.sleep(max(config.poll_interval_seconds, 5))


if __name__ == "__main__":
    main()
