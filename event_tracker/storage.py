"""Persistence layer for storing exhibition data locally."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from pydantic import BaseModel, Field

from .models import EventLink, StoredEvent, utcnow

DATA_DIRECTORY = Path("data")
DEFAULT_DATA_FILE = DATA_DIRECTORY / "events.json"


class StoragePayload(BaseModel):
    """Represents the JSON payload that we persist to disk."""

    events: List[StoredEvent] = Field(default_factory=list)
    last_updated_at: str | None = None

    def to_dict(self) -> dict:
        return self.model_dump()

    @classmethod
    def from_dict(cls, payload: dict) -> "StoragePayload":
        return cls.model_validate(payload or {})


class EventRepository:
    """File-based repository for storing exhibition data."""

    def __init__(self, data_file: Path = DEFAULT_DATA_FILE) -> None:
        self.data_file = data_file
        DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    def load(self) -> StoragePayload:
        if not self.data_file.exists():
            return StoragePayload(events=[], last_updated_at=None)
        with self.data_file.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return StoragePayload.from_dict(payload)

    def save(self, payload: StoragePayload) -> None:
        with self.data_file.open("w", encoding="utf-8") as handle:
            json.dump(payload.to_dict(), handle, ensure_ascii=False, indent=2)

    def add_new_events(self, links: Iterable[EventLink]) -> List[StoredEvent]:
        snapshot = self.load()
        known_urls = {event.url for event in snapshot.events}
        new_entries: List[StoredEvent] = []
        for link in links:
            if link.url in known_urls:
                continue
            stored = StoredEvent.from_link(link, timestamp=utcnow())
            new_entries.append(stored)
            snapshot.events.insert(0, stored)
            known_urls.add(link.url)
        snapshot.last_updated_at = utcnow().isoformat()
        self.save(snapshot)
        return new_entries
