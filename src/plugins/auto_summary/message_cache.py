import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List
from nonebot import get_driver

BASE_DIR = Path(__file__).parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "auto_summary"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = DATA_DIR / "cached_messages.json"

class MessageCache:
    def __init__(self):
        self._cache: Dict[int, List[str]] = defaultdict(list)
        self._load()

    def _load(self):
        if CACHE_FILE.exists():
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._cache = defaultdict(list, {int(k): v for k, v in data.items()})

    def _save(self):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({str(k): v for k, v in self._cache.items()}, f, ensure_ascii=False, indent=2)

    def add_message(self, group_id: int, user_id: int, msg: str):
        from .config import plugin_config
        if not plugin_config.auto_summary_enabled:
            return
        if not msg or len(msg) > 500:
            return
        self._cache[group_id].append(f"[用户{user_id}] {msg}")
        max_cache = plugin_config.auto_summary_max_cache
        if len(self._cache[group_id]) > max_cache:
            self._cache[group_id] = self._cache[group_id][-max_cache:]
        self._save()

    def get_and_clear(self, group_id: int) -> List[str]:
        messages = self._cache.pop(group_id, [])
        self._save()
        return messages

    def get_all_groups(self) -> List[int]:
        return list(self._cache.keys())

    def clear_group(self, group_id: int):
        if group_id in self._cache:
            del self._cache[group_id]
            self._save()

cache = MessageCache()