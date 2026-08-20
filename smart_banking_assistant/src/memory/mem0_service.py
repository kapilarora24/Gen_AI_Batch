"""
Mem0 integration for long-term user memory.
The integration is deliberately fail-safe:
- MEM0_ENABLED=false (default) means no memory calls are made.
- MEM0_API_KEY enables Mem0 Cloud through MemoryClient when available.
- Without a cloud key, MEM0_LOCAL=true can use the OSS Memory class.
All memory failures are logged and converted to an empty result so the
banking graph does not fail because the optional memory subsystem is down.
"""

from __future__ import annotations
import logging
import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class Mem0Service:
    def __init__(self) -> None:
        self.enabled = os.getenv("MEM0_ENABLED", "false").lower() == "true"
        self._client: Any | None = None
        self._mode: str | None = None
        if not self.enabled:
            return
        api_key = os.getenv("MEM0_API_KEY")
        try:
            if api_key:
                from mem0 import MemoryClient

                self._client = MemoryClient(api_key=api_key)
                self._mode = "cloud"
            elif os.getenv("MEM0_LOCAL", "false").lower() == "true":
                from mem0 import Memory

                self._client = Memory()
                self._mode = "local"
            else:
                logger.warning(
                    "MEM0_ENABLED=true but MEM0_API_KEY/MEM0_LOCAL is not configured. "
                    "Mem0 will remain disabled."
                )
        except Exception:
            logger.exception("Unable to initialize Mem0; continuing without memory.")
            self._client = None

    @property
    def available(self) -> bool:
        return self._client is not None

    def _user_id(self, account_id: str | None, thread_id: str | None) -> str:
        return account_id or thread_id or "anonymous"

    def search(
        self,
        query: str,
        account_id: str | None = None,
        thread_id: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        if not self.available or not query.strip():
            return []
        user_id = self._user_id(account_id, thread_id)
        try:
            if self._mode == "cloud":
                result = self._client.search(
                    query=query,
                    user_id=user_id,
                    limit=limit,
                )
            else:
                result = self._client.search(
                    query,
                    user_id=user_id,
                    limit=limit,
                )
            return self._normalize_results(result)
        except Exception:
            logger.exception("Mem0 search failed for user_id=%s", user_id)
            return []

    def add_turn(
        self,
        question: str,
        answer: str,
        account_id: str | None = None,
        thread_id: str | None = None,
    ) -> bool:
        if not self.available or not question.strip() or not answer.strip():
            return False
        user_id = self._user_id(account_id, thread_id)
        messages = [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
        try:
            self._client.add(messages, user_id=user_id)
            return True
        except Exception:
            logger.exception("Mem0 write failed for user_id=%s", user_id)
            return False

    @staticmethod
    def _normalize_results(result: Any) -> list[dict[str, Any]]:
        if result is None:
            return []
        if isinstance(result, dict):
            items = result.get("results", result.get("memories", []))
        else:
            items = result
        if not isinstance(items, list):
            return []
        normalized: list[dict[str, Any]] = []
        for item in items:
            if isinstance(item, str):
                normalized.append({"memory": item})
            elif isinstance(item, dict):
                text = (
                    item.get("memory") or item.get("text") or item.get("content") or ""
                )
                if text:
                    normalized.append(
                        {
                            "memory": text,
                            "id": item.get("id"),
                            "score": item.get("score"),
                        }
                    )
        return normalized


mem0_service = Mem0Service()
