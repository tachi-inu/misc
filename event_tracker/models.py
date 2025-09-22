"""Data models used by the exhibition tracker."""
from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict


def utcnow() -> datetime:
    """Return the current time in UTC with timezone information."""
    return datetime.now(timezone.utc)


class EventLink(BaseModel):
    """Represents an event link fetched from the website."""

    model_config = ConfigDict(frozen=True)

    title: str
    url: str

    def as_dict(self) -> dict:
        """Return a serialisable representation."""
        return self.model_dump()


class StoredEvent(BaseModel):
    """Represents a locally stored event entry."""

    model_config = ConfigDict(frozen=True)

    title: str
    url: str
    first_seen_at: str

    def as_dict(self) -> dict:
        """Return a serialisable representation."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, payload: dict) -> "StoredEvent":
        return cls.model_validate(payload)

    @classmethod
    def from_link(cls, link: EventLink, timestamp: datetime | None = None) -> "StoredEvent":
        ts = timestamp or utcnow()
        return cls(title=link.title, url=link.url, first_seen_at=ts.isoformat())
